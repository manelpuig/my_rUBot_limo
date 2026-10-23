# LIMO Navigation2

This package starts Nav2 localization and navigation on the Ubuntu 22.04 ROS 2
Humble PC. It is configured for the real Mecanum LIMO Pro and consumes `/scan`
and the public `/odom` interface from the Foxy robot. The raw wheel estimate
remains available on `/wheel/odom` for diagnostics.

Replace the placeholder map before driving:

```bash
ros2 launch limo_navigation2 navigation.launch.py \
  map:=/absolute/path/to/limo_map.yaml
```

The first real-robot tests must use low speeds and an accessible emergency stop.
