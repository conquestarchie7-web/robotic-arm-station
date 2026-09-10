"""Workspace and camera calibration utility for the Niryo Ned2.

The project reports state that a pointer/calibration tip was used to define the
four corners of workspace W1. PyNiryo 1.2.0 provides a direct API for saving a
workspace from four robot poses.
"""

from pyniryo import NiryoRobot

ROBOT_IP = "192.168.0.10"
WORKSPACE_NAME = "W1"


def save_w1(robot: NiryoRobot, pose_origin, pose_2, pose_3, pose_4) -> None:
    """Save W1 from the four calibrated corner poses."""
    robot.save_workspace_from_robot_poses(
        WORKSPACE_NAME,
        pose_origin,
        pose_2,
        pose_3,
        pose_4,
    )


def camera_calibration(robot: NiryoRobot):
    """Return the Ned2 camera intrinsics and distortion coefficients."""
    return robot.get_camera_intrinsics()


def main() -> None:
    robot = NiryoRobot(ip_address=ROBOT_IP)
    try:
        robot.connect(ROBOT_IP)
        if robot.need_calibration():
            robot.calibrate_auto()

        print("W1 calibration utility ready.")
        print("Move the calibration tip to the four W1 corners and record")
        print("the four poses, then pass them to save_w1().")
    finally:
        robot.close_connection()


if __name__ == "__main__":
    main()
