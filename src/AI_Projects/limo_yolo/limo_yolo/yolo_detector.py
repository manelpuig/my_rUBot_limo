import json

import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from std_msgs.msg import String
from ultralytics import YOLO
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose


class YoloDetector(Node):
    def __init__(self):
        super().__init__("yolo_detector")

        self.declare_parameter("image_topic", "/camera/color/image_raw")
        self.declare_parameter("model", "yolo11n.pt")
        self.declare_parameter("confidence", 0.35)
        self.declare_parameter("device", "cpu")
        self.declare_parameter("annotated_topic", "/limo_yolo/annotated_image")
        self.declare_parameter("detections_topic", "/limo_yolo/detections_2d")
        self.declare_parameter("detections_json_topic", "/limo_yolo/detections_json")
        self.declare_parameter("camera_info_topic", "/camera/color/camera_info")

        image_topic = self.get_parameter("image_topic").value
        model_name = self.get_parameter("model").value
        self.confidence = float(self.get_parameter("confidence").value)
        self.device = self.get_parameter("device").value
        annotated_topic = self.get_parameter("annotated_topic").value
        detections_topic = self.get_parameter("detections_topic").value
        detections_json_topic = self.get_parameter("detections_json_topic").value
        camera_info_topic = self.get_parameter("camera_info_topic").value

        self.bridge = CvBridge()
        self.model = YOLO(model_name)

        self.annotated_publisher = self.create_publisher(
            Image, annotated_topic, qos_profile_sensor_data
        )
        self.detections_publisher = self.create_publisher(
            Detection2DArray, detections_topic, 10
        )
        self.detections_json_publisher = self.create_publisher(
            String, detections_json_topic, 10
        )
        self.image_subscription = self.create_subscription(
            Image, image_topic, self.image_callback, qos_profile_sensor_data
        )
        self.camera_info = None
        self.camera_info_subscription = self.create_subscription(
            CameraInfo,
            camera_info_topic,
            self.camera_info_callback,
            qos_profile_sensor_data,
        )

        self.get_logger().info(f"YOLO model: {model_name}")
        self.get_logger().info(f"Image topic: {image_topic}")
        self.get_logger().info(f"Device: {self.device}")

    def camera_info_callback(self, message):
        """Keep the latest calibration for future 3D/depth extensions."""
        self.camera_info = message

    def image_callback(self, message):
        try:
            image = self.bridge.imgmsg_to_cv2(message, desired_encoding="bgr8")
            results = self.model.predict(
                source=image,
                conf=self.confidence,
                device=self.device,
                verbose=False,
            )
        except Exception as error:
            self.get_logger().error(f"YOLO inference failed: {error}")
            return

        detections = []
        detections_message = Detection2DArray()
        detections_message.header = message.header
        if results:
            result = results[0]
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls.item())
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    detections.append(
                        {
                            "class_id": class_id,
                            "class_name": result.names[class_id],
                            "confidence": float(box.conf.item()),
                            "bbox_xyxy": [x1, y1, x2, y2],
                        }
                    )
                    detection = Detection2D()
                    detection.header = message.header
                    detection.bbox.center.x = (x1 + x2) / 2.0
                    detection.bbox.center.y = (y1 + y2) / 2.0
                    detection.bbox.size_x = x2 - x1
                    detection.bbox.size_y = y2 - y1
                    hypothesis = ObjectHypothesisWithPose()
                    hypothesis.hypothesis.class_id = result.names[class_id]
                    hypothesis.hypothesis.score = float(box.conf.item())
                    detection.results.append(hypothesis)
                    detections_message.detections.append(detection)

            annotated = result.plot()
            annotated_message = self.bridge.cv2_to_imgmsg(
                annotated, encoding="bgr8"
            )
            annotated_message.header = message.header
            self.annotated_publisher.publish(annotated_message)

        self.detections_publisher.publish(detections_message)
        json_output = String()
        json_output.data = json.dumps(detections)
        self.detections_json_publisher.publish(json_output)


def main(args=None):
    rclpy.init(args=args)
    node = YoloDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
