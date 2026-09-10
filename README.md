# Robotic Arm Colour Sorting Station

Camera-guided automated colour sorting using a **Niryo Ned2**, Python, RoboDK, an IR conveyor sensor and an end-effector-mounted camera.

## Overview

The system was developed first in RoboDK simulation and then implemented on the physical Niryo Ned2. Objects are transported along a conveyor, detected by an IR sensor, observed by the robot-mounted camera, picked using the calibrated workspace, and placed into the correct colour zone.

The central engineering problem was **accurate camera-to-robot manipulation**: the robot needed not only to identify the object's colour, but to use its camera/workspace calibration to position the gripper accurately enough for a repeatable physical grasp.

Videos have been made available of a hardware demo:
https://youtube.com/shorts/vXRjFl9204E

And a simulation demo:
https://youtu.be/Iaszq8TXOIo

## Workflow

```text
Conveyor running
      ↓
IR sensor detects object
      ↓
Conveyor stops
      ↓
Robot moves to observation pose
      ↓
End-effector camera identifies object
      ↓
Vision-guided pick in W1
      ↓
Object colour retained
      ↓
RED / GREEN / BLUE destination selected
      ↓
Object placed
      ↓
Return to observation pose
      ↓
Repeat until max_object_count
```

## Key technical features

### Camera-guided picking

PyNiryo 1.2.0's `vision_pick()` combines camera detection, object approach, picking-height motion, gripper actuation and lifting. The implementation uses it with the calibrated `W1` workspace.

### Workspace calibration

The picking region is represented by workspace `W1`. The report describes calibrating its four corners using the robot and a pointer/calibration tip.

### Pick-height compensation

The final system required a **-0.01 m height offset** because the calibration reference points were slightly above the conveyor/object surface. The value was tuned through repeated physical testing.

### Sensor-driven conveyor control

The conveyor runs while the IR sensor is monitored. When an object reaches the sensor, the conveyor is stopped and the robot begins the vision/pick sequence.

### Deterministic colour sorting

The detected object colour maps directly to a corresponding destination:

```text
RED   → red zone
GREEN → green zone
BLUE  → blue zone
```

## Repository structure

```text
robotic-arm-station/
├── README.md
├── hardware/
│   ├── main_hardware.py
│   └── calibration.py
```

## Hardware

- Niryo Ned2 robot arm
- Niryo gripper
- Conveyor belt
- IR object-detection sensor
- End-effector-mounted camera
- Red, green and blue sorting zones
- Niryo Studio for calibration

## Running the hardware reference

1. Install the PyNiryo environment used by the Ned2.
2. Set `ROBOT_IP` / `Config.robot_ip` to the robot's address.
3. Calibrate the robot if required.
4. Calibrate workspace `W1`.
5. Populate `OBSERVATION_POSE` and the three colour drop poses.
6. Set the correct IR sensor pin for the laboratory wiring.
7. Run `hardware/main_hardware.py`.

The numerical poses and pin ID are intentionally not fabricated because they were not retained in the final report.

## Running the simulation reference

The original project used `Niryo.rdk` and a supplied `helpers_sim.py`. Those files were not retained, so a video recorded when the simulation was in development has been made available.

## Practical engineering lessons

The project demonstrated that robot accuracy is affected by more than the motion programme itself. The final report created identifies two especially important issues:

- **Lighting:** changes in laboratory lighting affected camera-based picking, leading to environmental standardisation during operation.
- **Calibration:** the gripper initially attempted to pick above the object. A small height offset was found experimentally to improve grasp reliability.

## Source reconstruction note

The original source code was not fully retained. This repository therefore distinguishes between:

- behaviour and structure explicitly documented in the project report;
- API calls aligned to the published PyNiryo 1.2.0 documentation;
- configuration values that must be recovered from the original physical setup.

No missing joint angles, workspace coordinates or sensor IDs have been invented.

## Technologies

**Python · PyNiryo · RoboDK · Niryo Ned2 · Computer Vision · Robot Manipulation · Workspace Calibration · Sensor Integration · Conveyor Automation · Pick and Place**
