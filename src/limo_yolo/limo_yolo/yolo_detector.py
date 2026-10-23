import json

import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_msgs.msg import String
from ultralytics import YOLO


class YoloDetector(Node):
    def __init__(self):
        super().__init__("yolo_detector")

        self.declare_parameter("image_topic", "/camera/color/image_raw")
        self.declare_parameter("model", "yolo11n.pt")
        self.declare_parameter("confidence", 0.35)
        self.declare_parameter("device", "cpu")
        self.declare_parameter("annotated_topic", "/limo_yolo/annotated_image")
        self.declare_parameter("detections_topic", "/limo_yolo/detections")

        image_topic = self.get_parameter("image_topic").value
        model_name = self.get_parameter("model").value
        self.confidence = float(self.get_parameter("confidence").value)
        self.device = self.get_parameter("device").value
        annotated_topic = self.get_parameter("annotated_topic").value
        detections_topic = self.get_parameter("detections_topic").value

        self.bridge = CvBridge()
        self.model = YOLO(model_name)

        self.annotated_publisher = self.create_publisher(
            Image, annotated_topic, qos_profile_sensor_data
        )
        self.detections_publisher = self.create_publisher(
            String, detections_topic, 10
        )
        self.image_subscription = self.create_subscription(
            Image, image_topic, self.image_callback, qos_profile_sensor_data
        )

        self.get_logger().info(f"YOLO model: {model_name}")
        self.get_logger().info(f"Image topic: {image_topic}")
        self.get_logger().info(f"Device: {self.device}")

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

            annotated = result.plot()
            annotated_message = self.bridge.cv2_to_imgmsg(
                annotated, encoding="bgr8"
            )
            annotated_message.header = message.header
            self.annotated_publisher.publish(annotated_message)

        output = String()
        output.data = json.dumps(detections)
        self.detections_publisher.publish(output)


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
