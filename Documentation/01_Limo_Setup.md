# 1. LIMO Pro and control PC setup

## 1. System overview

This guide explains how to prepare and test the complete project.

| Computer | Operating system | ROS 2 | Main role |
|---|---|---|---|
| LIMO Pro | Jetson Orin Nano, Ubuntu 20.04 | Foxy | Mecanum base, IMU, YDLidar and Orbbec DaBai |
| Control PC | Ubuntu 22.04 | Humble | Teleoperation, visualization, navigation and applications |

The branch contains all project packages. The robot builds only the packages
needed for hardware bringup. The control PC builds the complete workspace.

Working branch:

```text
refactor/real-limo-bringup-humble
```

Do not remove or overwrite the Foxy workspace that already works on the robot.
Test this branch in a new directory.

## 2. LIMO Pro setup

### 2.1. Clone the branch into a separate workspace

```bash
cd ~
git clone \
  --branch refactor/real-limo-bringup-humble \
  --single-branch \
  https://github.com/manelpuig/my_rUBot_limo.git \
  limo_refactor_ws

cd ~/limo_refactor_ws
git status --short --branch
```

`git status` must show the `refactor/real-limo-bringup-humble` branch.

### 2.2. Load ROS 2 Foxy and check the robot

```bash
source /opt/ros/foxy/setup.bash
cd ~/limo_refactor_ws
bash scripts/limo_preflight.sh
```

The check should find:

- `ROS_DISTRO=foxy`
- Base port `/dev/ttyTHS0`
- LiDAR link `/dev/ydlidar`
- Orbbec USB device

Do not continue if a device is missing. First check its port and permissions.

### 2.3. Install dependencies

Initialize `rosdep` only if it has not been initialized before:

```bash
sudo rosdep init
```

If it reports that `rosdep` is already initialized, continue with:

```bash
rosdep update
source /opt/ros/foxy/setup.bash
cd ~/limo_refactor_ws

rosdep install --ignore-src -r -y --rosdistro foxy --from-paths \
  src/Robot_drivers/limo_msgs \
  src/Robot_drivers/limo_base \
  src/Robot_drivers/ydlidar_ros2_driver \
  src/Robot_drivers/rf2o_laser_odometry \
  src/Robot_drivers/OrbbecSDK_ROS2/orbbec_camera_msgs \
  src/Robot_drivers/OrbbecSDK_ROS2/orbbec_camera \
  src/Robot_drivers/OrbbecSDK_ROS2/orbbec_description
```

The YDLidar driver needs the YDLidar SDK. Check if the working robot already
has it:

```bash
ldconfig -p | grep -i ydlidar
```

If it is missing, follow `src/Robot_drivers/YDLidar-SDK/README.md`. Do not replace a working
SDK installation without a reason.

### 2.4. Build only the robot bringup

```bash
source /opt/ros/foxy/setup.bash
cd ~/limo_refactor_ws
colcon build --symlink-install --packages-up-to limo_bringup
source install/setup.bash
```

This builds the bringup and its workspace dependencies. It does not build the
simulation, navigation, YOLO or vision exercises.

In every new robot terminal, run:

```bash
source /opt/ros/foxy/setup.bash
source ~/limo_refactor_ws/install/setup.bash
```

## 3. First robot bringup

For the first movement tests, lift the wheels off the floor and be ready to
stop the robot.

### 3.1. Test the base only

```bash
ros2 launch limo_bringup limo_robot_base.launch.py \
  port_name:=ttyTHS0 \
  use_mecanum:=true \
  publish_odom_tf:=true
```

In a second robot terminal:

```bash
source /opt/ros/foxy/setup.bash
source ~/limo_refactor_ws/install/setup.bash
ros2 topic echo /limo_status
```

Use separate terminals for these checks:

```bash
ros2 topic hz /wheel/odom
ros2 topic hz /imu
ros2 run tf2_ros tf2_echo odom base_link
```

The test is correct when:

- The serial port opens without errors.
- `/limo_status` publishes data.
- `/wheel/odom` and `/imu` update continuously.
- Only one node publishes `odom -> base_link`.

### 3.2. Test the YDLidar only

```bash
ros2 launch limo_bringup limo_robot_lidar.launch.py
```

Check:

```bash
ros2 topic hz /scan
ros2 run tf2_ros tf2_echo base_link laser_link
```

The initial value `laser_z:=0.02` comes from the previous driver launcher.
Measure the real LiDAR position before using this TF as a final value.

### 3.3. Test the DaBai camera only

```bash
ros2 launch limo_bringup limo_robot_camera.launch.py
```

Check the camera topics:

```bash
ros2 topic list | grep camera
```

The `base_link -> camera_link` mounting TF is disabled until the real camera
position and orientation are measured.

### 3.4. Start the complete bringup

After all three separate tests work:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py \
  base_port:=ttyTHS0 \
  use_mecanum:=true \
  use_lidar:=true \
  use_camera:=true \
  use_rf2o:=false \
  publish_odom_tf:=true \
  publish_camera_mount_tf:=false
```

These are the default values. After checking them, the short command is:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py
```

RF2O is disabled for the first tests. This avoids a second odometry and TF
source.

Quick checks:

```bash
ros2 node list
ros2 topic list
ros2 topic hz /wheel/odom
ros2 topic hz /imu
ros2 topic hz /scan
ros2 run tf2_ros tf2_echo odom base_link
ros2 run tf2_ros tf2_echo base_link laser_link
```

After the manual bringup works, automatic startup can be configured with
[1_Install_ros2foxy_service.md](files/Install_Limo/1_Install_ros2foxy_service.md).

## 4. Ubuntu 22.04 control PC setup

### 4.1. Install basic tools

```bash
sudo apt update
sudo apt install -y \
  git \
  python3-colcon-common-extensions \
  python3-rosdep \
  ros-humble-teleop-twist-keyboard
```

Initialize `rosdep` only if needed:

```bash
sudo rosdep init
rosdep update
```

### 4.2. Clone the same branch

```bash
cd ~
git clone \
  --branch refactor/real-limo-bringup-humble \
  --single-branch \
  https://github.com/manelpuig/my_rUBot_limo.git \
  limo_humble_ws

cd ~/limo_humble_ws
git status --short --branch
```

### 4.3. Install dependencies and build all packages

```bash
source /opt/ros/humble/setup.bash
cd ~/limo_humble_ws
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
ldconfig -p | grep -i ydlidar
colcon build --symlink-install
source install/setup.bash
```

If `ldconfig` cannot find `ydlidar_sdk`, install it by following
`src/Robot_drivers/YDLidar-SDK/README.md` before running `colcon build`.

This command builds the complete repository. If an optional package fails,
save the first `colcon` error and fix its dependency. Do not remove the package
from the branch.

In every new PC terminal, run:

```bash
source /opt/ros/humble/setup.bash
source ~/limo_humble_ws/install/setup.bash
```

## 5. Foxy-to-Humble communication

The robot and control PC must be connected to the same local network. For the
first test, use the default DDS implementation and the same ROS domain.

Run this on both the robot and the PC:

```bash
export ROS_DOMAIN_ID=10
export ROS_LOCALHOST_ONLY=0
```

These settings are temporary. Do not add them to `.bashrc` until communication
has been tested.

Start the bringup on the robot. Then check from the PC:

```bash
ros2 node list
ros2 topic list
ros2 topic echo /limo_status
ros2 topic hz /wheel/odom
ros2 topic hz /scan
ros2 topic info /cmd_vel --verbose
```

If the PC cannot see the robot topics, check on both computers:

```bash
printenv ROS_DOMAIN_ID
printenv ROS_LOCALHOST_ONLY
printenv RMW_IMPLEMENTATION
hostname -I
```

Both computers must use the same `ROS_DOMAIN_ID`. A firewall or Wi-Fi network
that blocks multicast can also stop ROS discovery.

## 6. First keyboard teleoperation

Lift the robot wheels off the floor for the first test. Keep the robot bringup
running, then execute this on the PC:

```bash
source /opt/ros/humble/setup.bash
source ~/limo_humble_ws/install/setup.bash
export ROS_DOMAIN_ID=10
export ROS_LOCALHOST_ONLY=0

ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p speed:=0.10 -p turn:=0.30
```

In another PC terminal, check the commands:

```bash
ros2 topic echo /cmd_vel
```

Use short movements and check that:

- The wheels stop when no command is sent.
- Forward and backward directions are correct.
- Side movement works as expected for a Mecanum base.
- Rotation direction is correct.
- `/limo_status`, `/wheel/odom`, `/imu` and `/scan` keep publishing.

Stop immediately if a wheel moves in the wrong direction, the robot does not
stop, or serial communication errors appear.

## 7. Update the branch later

Do not clone the repository again. Update the existing workspace:

```bash
cd ~/limo_refactor_ws     # robot
# or: cd ~/limo_humble_ws  # PC
git pull --ff-only
```

Build again after an update and source `install/setup.bash`.

## References

- AgileX LIMO ROS 2: <https://github.com/agilexrobotics/limo_ros2>
- LIMO Pro ROS 2 Foxy manual:
  <https://github.com/agilexrobotics/limo_pro_doc/blob/master/Limo%20Pro%20Ros2%20Foxy%20user%20manual(EN).md>
- YDLidar ROS 2: <https://github.com/YDLIDAR/ydlidar_ros2_driver>
- Orbbec ROS 2: <https://github.com/orbbec/OrbbecSDK_ROS2>
