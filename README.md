# my_rUBot_limo

ROS 2 workspace for AgileX LIMO + Orbbec camera + YDLidar (teaching/lab).

## Requirements
- Ubuntu 22.04
- ROS 2 Humble
- colcon, rosdep

## Clone
```bash
git clone https://github.com/manelpuig/my_rUBot_limo.git
cd my_rUBot_limo
```

## Build
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
