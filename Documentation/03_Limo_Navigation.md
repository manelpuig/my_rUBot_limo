# 3. LIMO Pro mapping with Cartographer

Cartographer runs on the Ubuntu 22.04 ROS 2 Humble control PC. The LIMO Pro
only runs the Foxy hardware bringup.

This is an initial configuration that must be tuned with the real robot.

## 1. Data flow

```text
LIMO Pro (Foxy)                 Control PC (Humble)
/scan             -----------> Cartographer
/wheel/odom       -----------> Cartographer
odom -> base_link -----------> TF
/cmd_vel          <----------- teleoperation or Nav2
```

Cartographer publishes the map and the `map -> odom` transform.

## 2. Install Cartographer on the PC

```bash
sudo apt update
sudo apt install -y ros-humble-cartographer ros-humble-cartographer-ros
```

Build the mapping and navigation packages:

```bash
source /opt/ros/humble/setup.bash
cd ~/limo_humble_ws
colcon build --symlink-install --packages-select \
  limo_cartographer limo_navigation2 limo_nav_control
source install/setup.bash
```

## 3. Check robot data

Start the normal bringup on the LIMO Pro. On the PC:

```bash
export ROS_DOMAIN_ID=10
export ROS_LOCALHOST_ONLY=0

ros2 topic hz /scan
ros2 topic hz /wheel/odom
ros2 run tf2_ros tf2_echo odom base_link
ros2 run tf2_ros tf2_echo base_link laser_link
```

Do not start Cartographer until all four checks work.

## 4. Start Cartographer

```bash
source /opt/ros/humble/setup.bash
source ~/limo_humble_ws/install/setup.bash
export ROS_DOMAIN_ID=10
export ROS_LOCALHOST_ONLY=0

ros2 launch limo_cartographer cartographer.launch.py
```

The launcher uses:

- `/scan`
- `/wheel/odom`
- `base_link`
- `odom`
- `map`
- Real time (`use_sim_time:=false`)

Start without RViz if needed:

```bash
ros2 launch limo_cartographer cartographer.launch.py use_rviz:=false
```

## 5. Create a map

Drive slowly with keyboard teleoperation. Avoid fast rotations and repeated
movement through people or moving objects.

Check:

```bash
ros2 topic hz /map
ros2 run tf2_ros tf2_echo map odom
```

Save the map:

```bash
mkdir -p ~/limo_humble_ws/maps
ros2 run nav2_map_server map_saver_cli \
  -f ~/limo_humble_ws/maps/limo_lab
```

This creates `limo_lab.yaml` and `limo_lab.pgm`.

## 6. Parameters to tune on the real robot

Edit `src/Navigation_Projects/limo_cartographer/config/limo_lds_2d.lua` only after recording the
problem and the test conditions. Main parameters:

- `TRAJECTORY_BUILDER_2D.min_range`
- `TRAJECTORY_BUILDER_2D.max_range`
- `missing_data_ray_length`
- `motion_filter.max_angle_radians`
- `constraint_builder.min_score`

The initial maximum range is `16.0 m`. It must be adjusted to the exact
YDLidar model and the laboratory environment.

## 7. Prepare the saved map for Nav2

Copy the map created in section 5 into the navigation package:

```bash
cp ~/limo_humble_ws/maps/limo_lab.yaml \
  ~/limo_humble_ws/src/Navigation_Projects/limo_navigation2/map/limo_map.yaml
cp ~/limo_humble_ws/maps/limo_lab.pgm \
  ~/limo_humble_ws/src/Navigation_Projects/limo_navigation2/map/limo_map.pgm
```

Check that the `image:` line in `limo_map.yaml` is `limo_map.pgm`, then rebuild
`limo_navigation2`. The map included in Git is only a small placeholder.

## 8. Start Nav2 localization and navigation

Keep the Foxy bringup running on the robot. On the Humble PC:

```bash
source /opt/ros/humble/setup.bash
source ~/limo_humble_ws/install/setup.bash
export ROS_DOMAIN_ID=10
export ROS_LOCALHOST_ONLY=0

ros2 launch limo_navigation2 navigation.launch.py
```

The initial configuration uses `base_link`, `/wheel/odom`, `/scan`, `/cmd_vel`
and the AMCL omnidirectional motion model. DWB samples X, Y and angular velocity
for the Mecanum base. Speeds and the footprint are deliberately conservative
and must be checked on the real robot.

Set the initial pose in RViz, then send a small nearby goal. Keep the emergency
stop accessible during every first test.

## 9. Run a waypoint mission

Edit this file so all points are inside free map space:

```text
src/Navigation_Projects/limo_nav_control/config/waypoints_real.yaml
```

Then run:

```bash
ros2 launch limo_nav_control waypoint_mission.launch.py
```

The node sets the optional initial pose, waits for Nav2, follows the waypoint
list, reports progress and cancels the mission after the configured timeout.

The Nav2 parameters are an initial test configuration. Do not use the old
Ackermann configuration for the Mecanum LIMO Pro.
