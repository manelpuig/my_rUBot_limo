# Source tree

The ROS package name is independent from its folder depth. `colcon` finds the
packages recursively.

- `Robot_drivers`: LIMO base, messages, YDLidar, Orbbec and optional RF2O.
- `limo_bringup`: robot launch files.
- `limo_description`: URDF and meshes.
- `Navigation_Projects`: Cartographer, Nav2 and waypoint missions.
- `AI_Projects`: YOLO11 and older vision examples.
- `Simulation`: simulation-only packages.

`limo_gazebo_classic` is the old Ackermann Gazebo Classic simulation. It is not
the mecanum Gazebo Sim implementation planned for later work.

The unused `csm` package and the superseded `yolov5_ros2` package were removed.
YOLO work is now concentrated in `AI_Projects/limo_yolo`.
