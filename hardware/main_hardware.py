"""Niryo Ned2 automated colour-sorting station.

This is a reconstructed reference implementation based on the project report
and PyNiryo 1.2.0 documentation. It is not claimed to be the original source.

Documented workflow:
    conveyor -> IR detection -> observation pose -> vision pick ->
    colour-specific placement -> return -> repeat
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pyniryo import (
    NiryoRobot,
    ConveyorDirection,
    ObjectColor,
    ObjectShape,
    PinState,
    PoseObject,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Config:
    robot_ip: str = "192.168.0.10"
    workspace_name: str = "W1"
    ir_sensor_pin: str = "A1"
    conveyor_speed: int = 50
    max_object_count: int = 6
    arm_speed_percent: int = 50
    pick_height_offset_m: float = -0.01
    object_wait_timeout_s: float = 30.0
    failed_pick_retry_delay_s: float = 0.5


CONFIG = Config()


# Exact drop poses / observation pose from the student project were not
# retained in the report. Keep them in one place so the physical setup can be
# calibrated without changing the control logic below.
OBSERVATION_POSE: Optional[PoseObject] = None
RED_DROP_POSE: Optional[PoseObject] = None
GREEN_DROP_POSE: Optional[PoseObject] = None
BLUE_DROP_POSE: Optional[PoseObject] = None

SORT_POSES = {
    ObjectColor.RED: RED_DROP_POSE,
    ObjectColor.GREEN: GREEN_DROP_POSE,
    ObjectColor.BLUE: BLUE_DROP_POSE,
}


# ---------------------------------------------------------------------------
# Connection / calibration
# ---------------------------------------------------------------------------

def connect_and_prepare(robot: NiryoRobot, cfg: Config) -> None:
    robot.connect(cfg.robot_ip)

    if robot.need_calibration():
        robot.calibrate_auto()

    robot.set_arm_max_velocity(cfg.arm_speed_percent)


def validate_configuration() -> None:
    if OBSERVATION_POSE is None:
        raise RuntimeError(
            "OBSERVATION_POSE is not configured. The original project report "
            "does not contain the calibrated numeric value."
        )

    missing = [colour.name for colour, pose in SORT_POSES.items() if pose is None]
    if missing:
        raise RuntimeError(
            "Missing calibrated drop poses: " + ", ".join(missing)
        )


# ---------------------------------------------------------------------------
# Conveyor / IR sensing
# ---------------------------------------------------------------------------

def wait_for_object(robot: NiryoRobot, conveyor_id, cfg: Config) -> None:
    """Run the conveyor until the IR sensor indicates an object is present."""
    robot.run_conveyor(
        conveyor_id,
        speed=cfg.conveyor_speed,
        direction=ConveyorDirection.FORWARD,
    )

    start = time.monotonic()

    try:
        # The project report describes the sensor as HIGH while no object is
        # detected and LOW once the object reaches the sensor.
        while robot.digital_read(cfg.ir_sensor_pin) == PinState.HIGH:
            if time.monotonic() - start > cfg.object_wait_timeout_s:
                raise TimeoutError("Timed out waiting for conveyor object")
            time.sleep(0.01)
    finally:
        robot.stop_conveyor(conveyor_id)


# ---------------------------------------------------------------------------
# Camera-guided picking
# ---------------------------------------------------------------------------

def move_to_observation(robot: NiryoRobot) -> None:
    """Move to the documented observation position above workspace W1."""
    assert OBSERVATION_POSE is not None
    robot.move(OBSERVATION_POSE)


def vision_pick(robot: NiryoRobot, cfg: Config):
    """Detect and pick an object using the Ned2 camera.

    PyNiryo 1.2.0 documents vision_pick() as a combined operation that detects
    an object, approaches it, moves to the picking height, actuates the tool,
    and lifts the object. It returns object_found, object_shape, object_color.
    """
    return robot.vision_pick(
        cfg.workspace_name,
        height_offset=cfg.pick_height_offset_m,
        shape=ObjectShape.ANY,
        color=ObjectColor.ANY,
        obs_pose=OBSERVATION_POSE,
    )


# ---------------------------------------------------------------------------
# Colour routing / placement
# ---------------------------------------------------------------------------

def place_object(robot: NiryoRobot, detected_colour: ObjectColor) -> None:
    """Place the object into the matching calibrated colour zone."""
    if detected_colour not in SORT_POSES:
        raise ValueError(f"Unsupported sorting colour: {detected_colour}")

    place_pose = SORT_POSES[detected_colour]
    if place_pose is None:
        raise RuntimeError(f"No drop pose configured for {detected_colour.name}")

    robot.place(place_pose)


# ---------------------------------------------------------------------------
# Main station cycle
# ---------------------------------------------------------------------------

def run_sorting_station(robot: NiryoRobot, conveyor_id, cfg: Config) -> int:
    """Execute the complete finite automated sorting cycle."""
    objects_placed = 0
    robot.close_gripper()

    while objects_placed < cfg.max_object_count:
        print(
            f"Waiting for object {objects_placed + 1}/"
            f"{cfg.max_object_count}..."
        )

        # 1. Wait for an object to arrive at the pick area.
        wait_for_object(robot, conveyor_id, cfg)

        # 2. Move the camera above the calibrated picking workspace.
        move_to_observation(robot)

        # 3. Use vision to locate and identify the object, then pick it.
        found, shape, colour = vision_pick(robot, cfg)

        if not found:
            print("No object found in workspace; retrying.")
            time.sleep(cfg.failed_pick_retry_delay_s)
            continue

        print(f"Picked object: shape={shape}, colour={colour}")

        # 4. Route the object to its colour-specific destination.
        place_object(robot, colour)
        objects_placed += 1

        print(
            f"Placed object {objects_placed}/"
            f"{cfg.max_object_count}."
        )

        # 5. Return to observation/start position for the next cycle.
        move_to_observation(robot)

    return objects_placed


def main() -> None:
    validate_configuration()

    robot = NiryoRobot(ip_address=CONFIG.robot_ip)
    conveyor_id = None

    try:
        print("Connecting to Niryo Ned2...")
        connect_and_prepare(robot, CONFIG)

        conveyor_id = robot.set_conveyor()

        total = run_sorting_station(robot, conveyor_id, CONFIG)
        print(f"Sorting complete: {total} objects placed.")

    except Exception as exc:
        print(f"Station stopped because of an error: {exc}")
        raise

    finally:
        if conveyor_id is not None:
            try:
                robot.stop_conveyor(conveyor_id)
                robot.unset_conveyor(conveyor_id)
            except Exception:
                pass

        robot.close_connection()


if __name__ == "__main__":
    main()
