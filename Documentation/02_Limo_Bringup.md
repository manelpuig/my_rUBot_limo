# 2. LIMO Pro bringup

This guide is for normal use after completing `01_Limo_Setup.md`.

## 1. Start the robot

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
| `use_camera` | `true` | Start Orbbec DaBai |
| `use_rf2o` | `false` | Start laser odometry |
| `publish_odom_tf` | `true` | Publish `odom -> base_link` from the base |
| `publish_camera_mount_tf` | `false` | Publish the measured camera mounting TF |

Example without the camera:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py use_camera:=false
```

## 2. Start hardware separately

Base only:

```bash
ros2 launch limo_bringup limo_robot_base.launch.py
```

LiDAR only:

```bash
ros2 launch limo_bringup limo_robot_lidar.launch.py
```

Camera only:

```bash
ros2 launch limo_bringup limo_robot_camera.launch.py
```

## 3. Basic checks

```bash
ros2 node list
ros2 topic list
ros2 topic echo /limo_status
ros2 topic hz /wheel/odom
ros2 topic hz /imu
ros2 topic hz /scan
```

Check TF:

```bash
ros2 run tf2_ros tf2_echo odom base_link
ros2 run tf2_ros tf2_echo base_link laser_link
```

There must be only one publisher for each TF. The base publishes
`odom -> base_link`; the LiDAR launcher publishes `base_link -> laser_link`.

## 4. RF2O

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

## 6. Troubleshooting

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
