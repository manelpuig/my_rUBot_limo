# 2. LIMO Pro bringup

This guide is for normal use after completing [01_Limo_Setup.md](01_Limo_Setup.md).
The real LIMO Pro runs the Foxy hardware bringup. Gazebo Sim and Gazebo Classic
run on the Ubuntu 22.04 Humble control PC.

## 1. Start the real robot

On the LIMO Pro:

```bash
source /opt/ros/foxy/setup.bash
source ~/limo_refactor_ws/install/setup.bash
export ROS_DOMAIN_ID=10
export ROS_LOCALHOST_ONLY=0
```

Start the complete hardware bringup:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py
```

Default configuration:

| Argument | Default | Purpose |
|---|---:|---|
| `base_port` | `ttyTHS0` | Base serial port |
| `use_mecanum` | `true` | Force Mecanum mode |
| `use_lidar` | `true` | Start YDLidar |
| `lidar_params_file` | YDLidar package file | YDLidar parameter file |
| `laser_z` | `0.02` | Temporary LiDAR height in metres |
| `use_camera` | `true` | Start Orbbec DaBai |
| `enable_point_cloud` | `true` | Enable the camera point cloud |
| `use_rf2o` | `false` | Start laser odometry |
| `publish_odom_tf` | `true` | Publish `odom -> base_link` from the base |
| `publish_camera_mount_tf` | `false` | Publish the measured camera mounting TF |

Example without the camera:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py use_camera:=false
```

For the first movement test, lift the wheels off the floor and be ready to stop
the robot. Do not enable RF2O until wheel odometry has been checked.

## 2. Start real hardware separately

Base only:

```bash
ros2 launch limo_bringup limo_robot_base.launch.py \
  port_name:=ttyTHS0 \
  use_mecanum:=true \
  publish_odom_tf:=true
```

LiDAR only:

```bash
ros2 launch limo_bringup limo_robot_lidar.launch.py
```

The LiDAR launcher accepts `params_file`, `base_frame`, `laser_frame` and the
mounting pose arguments `laser_x`, `laser_y`, `laser_z`, `laser_roll`,
`laser_pitch` and `laser_yaw`. Measure the real pose before treating the default
`laser_z:=0.02` as final.

Camera only:

```bash
ros2 launch limo_bringup limo_robot_camera.launch.py
```

The camera launcher accepts `camera_name`, `enable_point_cloud`,
`enable_colored_point_cloud` and camera mounting TF arguments. The mounting TF
is disabled by default because the real `base_link -> camera_link` pose still
has to be measured.

## 3. Check the real robot

```bash
ros2 node list
ros2 topic list
ros2 topic echo /limo_status
ros2 topic hz /wheel/odom
ros2 topic hz /imu
ros2 topic hz /scan
ros2 topic list | grep camera
```

Check TF:

```bash
ros2 run tf2_ros tf2_echo odom base_link
ros2 run tf2_ros tf2_echo base_link laser_link
```

There must be only one publisher for each dynamic TF. By default, the base is
the only source of `odom -> base_link`; the LiDAR launcher publishes
`base_link -> laser_link`. Do not start another odometry node that publishes
the same transform.

## 4. Optional RF2O laser odometry

RF2O is optional and disabled by default. When enabled, it publishes
`/rf2o/odom` and does not publish TF:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py use_rf2o:=true
ros2 topic echo /rf2o/odom
```

Do not use RF2O as the main odometry source until it has been compared with
`/wheel/odom`.

## 5. Automatic startup

After manual bringup works, follow:

[1_Install_ros2foxy_service.md](files/Install_Limo/1_Install_ros2foxy_service.md)

## 6. Start Gazebo Sim on the Humble PC

Install and build the simulation dependencies as described in
[05_Limo_Simulation.md](05_Limo_Simulation.md). Then run:

```bash
source /opt/ros/humble/setup.bash
source ~/limo_humble_ws/install/setup.bash
ros2 launch limo_bringup limo_bringup_sw.launch.py
```

This is the default software bringup. It uses the shared Mecanum model from
`limo_description` and exposes these main interfaces:

| Function | Topic |
|---|---|
| Velocity command | `/cmd_vel` |
| Wheel odometry | `/wheel/odom` |
| LiDAR | `/scan` |
| IMU | `/imu` |
| RGB image | `/camera/color/image_raw` |
| Camera calibration | `/camera/color/camera_info` |
| Transforms | `/tf`, `/tf_static` |
| Simulation clock | `/clock` |

Useful launch arguments:

| Argument | Default | Purpose |
|---|---:|---|
| `world` | `empty_world.sdf` | Absolute path to a Gazebo Sim world |
| `model` | shared LIMO Xacro | Absolute path to the robot model |
| `robot_name` | `limo` | Gazebo entity name |
| `use_rviz` | `true` | Start RViz |
| `x`, `y`, `yaw` | `0.0` | Initial planar pose |
| `z` | `0.16` | Initial height |

Check the simulated robot:

```bash
ros2 topic hz /clock
ros2 topic hz /wheel/odom
ros2 topic hz /scan
ros2 topic hz /imu
ros2 topic hz /camera/color/image_raw
ros2 run tf2_ros tf2_echo odom base_footprint
ros2 run tf2_ros tf2_echo base_footprint base_link
```

Send a slow command from another terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/limo_humble_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p speed:=0.10 -p turn:=0.30
```

## 7. Optional Gazebo Classic bringup

Gazebo Classic is kept only for compatibility. It uses the same Xacro model
with the Classic plugins selected by the launcher:

```bash
source /opt/ros/humble/setup.bash
source ~/limo_humble_ws/install/setup.bash
ros2 launch limo_bringup limo_bringup_sw_classic.launch.py
```

Its main arguments are `world`, `model`, `use_rviz`, `x`, `y`, `z` and `yaw`.
The default Classic world is `worlds/classic/empty_world.world`. Validate this
optional path on Ubuntu before relying on it.

## 8. Keep real and simulated robots isolated

The real and simulated robots intentionally use the same command and sensor
topic names. This allows navigation applications to change between hardware
and simulation without remapping topics.

Do not run both in the same `ROS_DOMAIN_ID`: a `/cmd_vel` command could reach
the real robot while testing the simulator. Stop the real bringup or assign a
different domain, for example:

```bash
# Simulation terminals only
export ROS_DOMAIN_ID=20
```

The real base normally publishes `odom -> base_link`. The simulator publishes
`odom -> base_footprint`, followed by the fixed `base_footprint -> base_link`
transform from the robot description. This difference is intentional.

## 9. Troubleshooting

Base serial port:

```bash
ls -l /dev/ttyTHS0
groups
```

LiDAR:

```bash
ls -l /dev/ydlidar
ros2 topic hz /scan
```

Camera:

```bash
lsusb | grep -i -E 'orbbec|2bc5'
ros2 topic list | grep camera
```

Service logs:

```bash
journalctl -u limo-bringup.service -b -e
```

Simulation discovery and clock:

```bash
printenv ROS_DOMAIN_ID
ros2 topic info /cmd_vel --verbose
ros2 topic echo /clock
```

If Gazebo starts without the robot, check the first spawn error and confirm
that `limo_description` and `limo_bringup` are installed and sourced. These
launchers are initial configurations and still require runtime validation on
Ubuntu 22.04 with the selected Gazebo version.
