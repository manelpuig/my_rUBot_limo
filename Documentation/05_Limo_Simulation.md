# 5. LIMO Pro simulation

Gazebo Sim is the default simulator. It runs on the Ubuntu 22.04 ROS 2 Humble
PC and uses the same ROS topics as the real LIMO whenever possible.

## 1. Install simulation packages

```bash
sudo apt update
sudo apt install -y ros-humble-ros-gz ros-humble-joint-state-publisher
```

Gazebo Classic is optional:

```bash
sudo apt install -y ros-humble-gazebo-ros-pkgs
```

## 2. Build

```bash
source /opt/ros/humble/setup.bash
cd ~/limo_humble_ws
colcon build --symlink-install --packages-select limo_description limo_bringup
source install/setup.bash
```

## 3. Start Gazebo Sim

```bash
ros2 launch limo_bringup limo_bringup_sw.launch.py
```

Useful arguments:

```bash
ros2 launch limo_bringup limo_bringup_sw.launch.py \
  use_rviz:=false x:=0.0 y:=0.0 yaw:=0.0
```

The main topics are:

- `/cmd_vel`
- `/wheel/odom`
- `/scan`
- `/imu`
- `/camera/color/image_raw`
- `/camera/color/camera_info`
- `/tf`
- `/clock`

Check the simulation:

```bash
ros2 topic hz /scan
ros2 topic echo /wheel/odom --once
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

The Gazebo Sim model uses planar velocity control. It supports Mecanum X, Y and
angular commands, but it is an initial functional model rather than a detailed
wheel-contact model.

## 4. Optional Gazebo Classic

The legacy Ackermann simulation is kept only for compatibility:

```bash
ros2 launch limo_bringup limo_bringup_sw_classic.launch.py
```

Only the exceptional Classic world uses a `classic` subdirectory. Both
simulators use the common `limo_description/urdf/limo.urdf.xacro` model. New
simulation work should target Gazebo Sim.
