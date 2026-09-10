"""
Reconstructed reference implementation: Niryo Ned2 automated colour sorting station.

IMPORTANT:
The original source code was not retained. This file reconstructs the documented
program structure and control flow from the final project report. Exact Niryo API
calls, joint positions and sensor IDs should therefore be adapted to the hardware
and software environment before execution.
"""

from dataclasses import dataclass
from enum import Enum


class Colour(Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    UNKNOWN = "UNKNOWN"


@dataclass
class RobotConfig:
    max_object_count: int = 6
    workspace_name: str = "W1"
    pick_z_offset: float = -0.01


class RobotInterface:
    """Abstraction over the Niryo Ned2 hardware/API used by the project."""

    def connect(self):
        raise NotImplementedError

    def move_to_pose(self, pose):
        raise NotImplementedError

    def move_joints(self, joints):
        raise NotImplementedError

    def conveyor_start(self):
        raise NotImplementedError

    def conveyor_stop(self):
        raise NotImplementedError

    def digital_read(self, sensor_pin_id):
        raise NotImplementedError

    def vision_pick(self, workspace_name):
        raise NotImplementedError

    def open_gripper(self):
        raise NotImplementedError

    def close_gripper(self):
        raise NotImplementedError

    def release_object(self):
        raise NotImplementedError


# The six joint angles and calibrated poses were recorded physically during the
# project but were not preserved in the report. Deliberately use placeholders.
INITIAL_JOINTS = [None, None, None, None, None, None]
OBSERVATION_POSE = None
PICKING_POSE = None

SORT_POSES = {
    Colour.RED: None,
    Colour.GREEN: None,
    Colour.BLUE: None,
}

SENSOR_PIN_ID = None


def wait_for_object(robot: RobotInterface):
    """Run the conveyor until the IR sensor detects an object."""
    robot.conveyor_start()

    while robot.digital_read(SENSOR_PIN_ID) is True:
        pass

    robot.conveyor_stop()


def identify_and_pick(robot: RobotInterface, workspace_name: str):
    """Perform the documented vision-guided pick and return detected colour."""
    detected_colour = robot.vision_pick(workspace_name)

    if detected_colour is None:
        return Colour.UNKNOWN

    colour_name = str(detected_colour).upper()
    for colour in Colour:
        if colour.value in colour_name:
            return colour

    return Colour.UNKNOWN


def place_object(robot: RobotInterface, colour: Colour):
    """Move to the colour-specific sorting location and release the object."""
    pose = SORT_POSES.get(colour)
    if pose is None:
        raise RuntimeError(f"Sorting pose for {colour.value} is not calibrated.")

    robot.move_to_pose(pose)
    robot.release_object()


def run_sorting_cycle(robot: RobotInterface, config: RobotConfig):
    """Execute the documented finite sorting loop."""
    objects_placed = 0

    robot.move_joints(INITIAL_JOINTS)

    while objects_placed < config.max_object_count:
        # 1. Wait for the IR sensor to detect an object on the conveyor.
        wait_for_object(robot)

        # 2. Move to the observation position above the conveyor.
        if OBSERVATION_POSE is not None:
            robot.move_to_pose(OBSERVATION_POSE)

        # 3. Identify and pick the object using the end-effector camera.
        colour = identify_and_pick(robot, config.workspace_name)

        if colour == Colour.UNKNOWN:
            print("Object colour not recognised; no placement performed.")
            continue

        # 4. Place in the corresponding red, green or blue area.
        place_object(robot, colour)
        objects_placed += 1

        # 5. Return to the initial configuration.
        robot.move_joints(INITIAL_JOINTS)

    robot.conveyor_stop()


if __name__ == "__main__":
    robot = RobotInterface()
    robot.connect()

    config = RobotConfig(
        max_object_count=6,
        workspace_name="W1",
        pick_z_offset=-0.01,
    )

    run_sorting_cycle(robot, config)
