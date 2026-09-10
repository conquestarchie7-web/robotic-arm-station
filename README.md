# Robotic Arm Colour Sorting Station

A robotic pick-and-place sorting system developed as a university group project using a **Niryo Ned2 robot arm**, **RoboDK**, Python, an IR object-detection sensor and a camera mounted on the robot end-effector.

The system detects objects arriving on a conveyor, identifies their colour using the camera, accurately picks them from a calibrated workspace, and places them into the corresponding red, green or blue sorting area.

> **Repository note:** The original project source files were not retained. The Python programs in this repository are a reconstructed reference implementation based on the final project report, including the documented control flow, variables, calibration approach and robot operations. They are intended to communicate the engineering design and software architecture rather than claim to be the verbatim original submission.

## Project overview

The project was developed in two stages:

1. **Digital simulation in RoboDK**
2. **Physical implementation using a Niryo Ned2**

The simulation was used to establish robot poses, conveyor behaviour, object detection, camera-based colour identification, picking and colour-specific placement before transferring the workflow to the physical robot.

The final system was able to repeatedly:

```text
Object arrives on conveyor
        ↓
IR sensor detects object
        ↓
Conveyor stops
        ↓
Robot moves to observation pose
        ↓
End-effector camera identifies object
and records its colour
        ↓
Robot moves to calibrated picking workspace
        ↓
Vision-guided pick
        ↓
Robot carries object to colour zone
        ↓
Red / Green / Blue placement selected
        ↓
Object released
        ↓
Robot returns to initial pose
        ↓
Repeat until required count reached
```

The project report states that the completed system worked reliably in both simulation and hardware. The main development challenges were **robot calibration, camera lighting consistency, IR-sensor timing and the vertical offset required for accurate gripping**.

## Technical focus

The central engineering challenge was coordinating:

- conveyor sensing,
- camera-based object identification,
- a calibrated robot workspace,
- robot pose transitions,
- gripper actuation,
- and accurate physical pick-and-place.

The camera was mounted on the robot end-effector, allowing the arm to observe the picking workspace and use the detected object's colour during the later placement stage.

## Hardware

The documented physical system included:

- Niryo Ned2 robotic arm
- Niryo gripper
- Conveyor belt connected to the robot base
- IR object-detection sensor
- End-effector-mounted camera
- Three colour-sorting zones
- Niryo Studio for calibration and setup
- VS Code / Python for the control program

## Software architecture

### Simulation

The original simulation workflow was documented as:

```text
simulation/
├── main_sim.py
├── helpers_sim.py        # supplied project helper functions
└── Niryo.rdk             # supplied RoboDK station layout
```

`main_sim.py` contained the project simulation logic. The workflow was divided into:

1. Pose definition
2. Object placement
3. IR/object detection
4. Object picking
5. Object placement

### Hardware

The hardware implementation was documented around `main_hardware.py`, with four main areas:

1. Definitions and movements
2. Sorting loop
3. Conveyor detection
4. Object picking and placement

The reconstructed implementation under `hardware/` mirrors that architecture.

## Calibration and accuracy

Calibration was a major part of the project.

A square workspace named `W1` was established around the picking region. The four corner positions were calibrated by moving a pointer attachment to the corresponding reference points and recording their locations.

A further vertical offset was required during vision-based picking because the calibration reference points were slightly above the physical height of the objects on the conveyor.

The report describes this offset as being tuned gradually through repeated testing until the gripper reached the required depth without contacting the conveyor.

## Environmental sensitivity

The mounted camera was sensitive to changes in lighting. Changes in room illumination could cause the robot to miss an object even when the motion code was otherwise correct.

The final testing therefore controlled the environment by standardising the lighting conditions, including the number of blinds closed and lights switched on in the lab.

This was an important practical lesson: **calibration and environmental conditions were part of the sensing system**, not just a setup detail.

## Design choices

### Finite sorting loop

The system uses a configurable maximum object count:

```python
while objects_placed < max_object_count:
    ...
```

This makes the required number of sorting cycles explicit rather than relying on an uncontrolled infinite loop.

### Event-driven conveyor control

The conveyor is allowed to run while the IR sensor is checked continuously. Once an object is detected, the conveyor is stopped and the robot takes over the cycle.

### Vision-guided picking

The camera provides object identification within the calibrated workspace. The detected colour is retained and used later to select the correct drop location.

### Colour-dependent placement

The sorting decision is a deterministic mapping:

```text
RED   → red sorting zone
GREEN → green sorting zone
BLUE  → blue sorting zone
```

## Reconstructed source

The files under `simulation/` and `hardware/` are deliberately separated from any claim about the original source.

The report confirms the project used:

- Python
- RoboDK
- a Niryo Ned2
- `main_sim.py`
- `helpers_sim.py`
- `main_hardware.py`
- an IR sensor
- a mounted camera
- a calibrated `W1` workspace
- a vision-pick operation
- a height offset for successful gripping

The exact original imports, API calls, joint-angle values, sensor IDs and helper-function implementation were not preserved in the available report. Where those details are required, the reconstructed source uses clearly marked placeholders.

## Future improvements

The original report identified two main extensions:

- **Dynamic object sensing**, allowing the system to operate over a wider range of environmental conditions.
- **Parallel conveyor/robot operation**, allowing the conveyor to prepare the next object while the robot is sorting the previous one.

A further natural extension would be closed-loop verification of successful gripping and placement using camera feedback.

## Project context

This project was completed as part of the Heriot-Watt University **B38RO Introduction to Robotics** group project. The project involved simulation, hardware development, calibration, integration and experimental testing.

## Technologies

**Python · RoboDK · Niryo Ned2 · Computer Vision · Robot Manipulation · Pick and Place · Sensor Integration · Workspace Calibration · Conveyor Automation · Mechatronics**
