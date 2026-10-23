# LIMO navigation control

This package runs a simple Nav2 waypoint mission from a YAML file.

```bash
ros2 launch limo_nav_control waypoint_mission.launch.py
```

Edit `config/waypoints_real.yaml` so every pose is in free space on the loaded
map. Poses use `[x, y, yaw_radians]`.
