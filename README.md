# my_rUBot_limo

ROS 2 workspace for the AgileX LIMO Pro, Orbbec DaBai and YDLidar.

The robot runs native Ubuntu 20.04 with ROS 2 Foxy. Mapping, Nav2, RViz and
YOLO11 run on an Ubuntu 22.04 ROS 2 Humble PC.

Start with [Documentation/01_Limo_Setup.md](Documentation/01_Limo_Setup.md).

## Source layout

- `src/Robot_drivers`: base, messages and sensor drivers.
- `src/limo_bringup`: Foxy robot bringup and legacy Humble launch files.
- `src/limo_description`: LIMO models and meshes.
- `src/Navigation_Projects`: Cartographer, Nav2 and waypoint control.
- `src/AI_Projects`: YOLO11 and other vision examples.
- `src/Simulation`: the legacy Gazebo Classic Ackermann simulation.

## Clone
```bash
git clone https://github.com/manelpuig/my_rUBot_limo.git
cd my_rUBot_limo
```

## Build all packages on the Humble PC
```bash
sudo rosdep init 2>/dev/null || true
rosdep update
rosdep install --from-paths src -i -y --rosdistro humble

source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Orbbec test

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch orbbec_camera dabai.launch.py
```
