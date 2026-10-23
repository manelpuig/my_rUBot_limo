# 4. LIMO Pro vision with YOLO11

The Orbbec DaBai runs on the LIMO Pro. YOLO11 runs on the Ubuntu 22.04 ROS 2
Humble control PC.

The initial `limo_yolo` package performs object detection and publishes:

- Annotated image: `/limo_yolo/annotated_image`
- Standard detections: `/limo_yolo/detections_2d`
- JSON detections: `/limo_yolo/detections_json`

## 1. Check the camera topic

Start the camera or complete bringup on the robot. On the control PC:

```bash
export ROS_DOMAIN_ID=10
export ROS_LOCALHOST_ONLY=0
ros2 topic list | grep camera
```

The default YOLO topic is:

```text
/camera/color/image_raw
```

Confirm the real DaBai topic before starting YOLO:

```bash
ros2 topic hz /camera/color/image_raw
```

## 2. Install YOLO11 dependencies on the PC

```bash
sudo apt update
sudo apt install -y ros-humble-cv-bridge ros-humble-rqt-image-view \
  ros-humble-vision-msgs python3-pip
python3 -m pip install --user ultralytics
```

Build the package:

```bash
source /opt/ros/humble/setup.bash
cd ~/limo_humble_ws
colcon build --symlink-install --packages-select limo_yolo
source install/setup.bash
```

## 3. Start YOLO11

```bash
export ROS_DOMAIN_ID=10
export ROS_LOCALHOST_ONLY=0

ros2 launch limo_yolo yolo11.launch.py
```

The default model is `yolo11n.pt` and the default device is `cpu`. Ultralytics
downloads the standard model the first time it is used if it is not cached.

Use a different camera topic:

```bash
ros2 launch limo_yolo yolo11.launch.py \
  image_topic:=/camera/color/image_raw
```

Use a local custom model:

```bash
ros2 launch limo_yolo yolo11.launch.py \
  model:=/absolute/path/to/best.pt
```

Use an NVIDIA GPU on a correctly configured PC:

```bash
ros2 launch limo_yolo yolo11.launch.py device:=0
```

Start with `device:=cpu`. Configure CUDA separately only after CPU inference
works.

## 4. Check the results

```bash
ros2 topic echo /limo_yolo/detections_2d
ros2 topic echo /limo_yolo/detections_json
ros2 topic hz /limo_yolo/annotated_image
```

View the annotated image:

```bash
ros2 run rqt_image_view rqt_image_view
```

Select `/limo_yolo/annotated_image` in the topic list.

Each JSON detection contains:

- `class_id`
- `class_name`
- `confidence`
- `bbox_xyxy`

## 5. Configuration

Default parameters are stored in:

```text
src/AI_Projects/limo_yolo/config/yolo11.yaml
```

Important parameters:

- `image_topic`
- `model`
- `confidence`
- `device`
- `annotated_topic`
- `detections_topic`
- `detections_json_topic`
- `camera_info_topic`

## 6. First-test recommendations

- Disable the DaBai point cloud if network bandwidth is too high.
- Test RGB reception before starting YOLO.
- Use `yolo11n.pt` and CPU for the first test.
- Measure image and detection frequency.
- Use `/limo_yolo/detections_2d` when another ROS node consumes detections.
- Use `/limo_yolo/detections_json` for simple inspection and logging.

The old `yolov5_ros2` package was removed after its standard detection output
was added to `limo_yolo`. The `limo_visions` examples remain separate under
`src/AI_Projects`.
