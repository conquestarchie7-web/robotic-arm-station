# Reconstruction Notes

The original final report describes the software architecture and control flow but does not contain the original source files.

The report explicitly identifies:

- `main_sim.py` as the project simulation program
- `helpers_sim.py` as supplied helper code
- `Niryo.rdk` as the supplied RoboDK station layout
- `main_hardware.py` as the hardware program
- `W1` as the calibrated picking workspace
- an end-effector-mounted camera
- IR-based conveyor object detection
- a `vision_pick` operation
- a -0.01 vertical pick offset
- colour-based red/green/blue placement
- a finite sorting loop controlled by `max_object_count`

Exact:
- joint angle values,
- pose coordinates,
- sensor pin IDs,
- Niryo API imports,
- helper-function implementations,
- and the exact RoboDK station file

were not preserved in the available report.

For that reason, placeholders are used rather than fabricated numerical or API details.
