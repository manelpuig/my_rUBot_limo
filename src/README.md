# Source tree

The ROS package name is independent from its folder depth. `colcon` finds the
packages recursively.

- `Robot_drivers`: LIMO base, messages, YDLidar, Orbbec and optional RF2O.
- `limo_bringup`: real and simulated launchers, worlds and RViz files. Gazebo
  Sim resources use short default paths; only Gazebo Classic uses a `classic`
  subdirectory.
- `limo_description`: one common Mecanum model. Gazebo Sim is enabled by
  default; the same Xacro selects Classic plugins with `use_gz:=false`.
- `Navigation_Projects`: Cartographer, Nav2 and waypoint missions.
- `AI_Projects`: YOLO11 and older vision examples.
The unused `csm`, `limo_gazebo_classic` and superseded `yolov5_ros2` packages
were removed.
YOLO work is now concentrated in `AI_Projects/limo_yolo`.
