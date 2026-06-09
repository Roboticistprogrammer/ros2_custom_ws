"""ROS 2 YOLOv11 pallet detector node."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import PackageNotFoundError
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO
from vision_msgs.msg import Detection2D
from vision_msgs.msg import Detection2DArray
from vision_msgs.msg import ObjectHypothesisWithPose


PACKAGE_NAME = 'yolov11_warehouse_pallet_detector'
DEFAULT_MODEL_NAME = 'whole_pallet_n_640.pt'


def get_default_model_path():
    """Return the installed model path, falling back to the source tree."""
    try:
        package_share = Path(get_package_share_directory(PACKAGE_NAME))
        installed_model = package_share / 'models' / DEFAULT_MODEL_NAME
        if installed_model.exists():
            return str(installed_model)
    except PackageNotFoundError:
        pass

    package_dir = Path(__file__).resolve().parent
    source_model = package_dir.parent / 'models' / DEFAULT_MODEL_NAME
    return str(source_model)


class Yolov11Detector(Node):
    """Subscribe to camera images and publish YOLOv11 pallet detections."""

    def __init__(self):
        super().__init__('yolov11_detector')

        self.declare_parameter('model_path', get_default_model_path())
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('annotated_image_topic', '/camera/detections/image')
        self.declare_parameter('detections_topic', '/camera/detections')
        self.declare_parameter('confidence_threshold', 0.25)
        self.declare_parameter('device', '')
        self.declare_parameter('use_sim_time', False)

        model_path = self.get_parameter('model_path').value
        image_topic = self.get_parameter('image_topic').value
        annotated_topic = self.get_parameter('annotated_image_topic').value
        detections_topic = self.get_parameter('detections_topic').value
        self.confidence_threshold = float(
            self.get_parameter('confidence_threshold').value
        )
        self.device = str(self.get_parameter('device').value)

        if not Path(model_path).is_file():
            raise FileNotFoundError(f'YOLOv11 model not found: {model_path}')

        self.bridge = CvBridge()
        self.model = YOLO(model_path)
        self.image_subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10,
        )
        self.annotated_image_publisher = self.create_publisher(
            Image,
            annotated_topic,
            10,
        )
        self.detections_publisher = self.create_publisher(
            Detection2DArray,
            detections_topic,
            10,
        )

        self.get_logger().info(
            f'YOLOv11 detector ready: model={model_path}, image_topic={image_topic}'
        )

    def image_callback(self, msg):
        """Run YOLOv11 on a camera frame and publish detections."""
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        predict_kwargs = {
            'conf': self.confidence_threshold,
            'verbose': False,
        }
        if self.device:
            predict_kwargs['device'] = self.device

        results = self.model(cv_image, **predict_kwargs)
        result = results[0]

        detection_array = self._to_detection_array(result, msg.header)
        self.detections_publisher.publish(detection_array)

        annotated_frame = result.plot()
        annotated_msg = self.bridge.cv2_to_imgmsg(annotated_frame, encoding='bgr8')
        annotated_msg.header = msg.header
        self.annotated_image_publisher.publish(annotated_msg)

    def _to_detection_array(self, result, header):
        """Convert one Ultralytics result into a Detection2DArray message."""
        detection_array = Detection2DArray()
        detection_array.header = header

        names = result.names or {}
        boxes = result.boxes
        if boxes is None:
            return detection_array

        for box in boxes:
            xywh = box.xywh[0].tolist()
            class_index = int(box.cls[0].item())
            score = float(box.conf[0].item())

            detection = Detection2D()
            detection.header = header
            detection.bbox.center.position.x = float(xywh[0])
            detection.bbox.center.position.y = float(xywh[1])
            detection.bbox.center.theta = 0.0
            detection.bbox.size_x = float(xywh[2])
            detection.bbox.size_y = float(xywh[3])

            hypothesis = ObjectHypothesisWithPose()
            hypothesis.hypothesis.class_id = str(names.get(class_index, class_index))
            hypothesis.hypothesis.score = score
            detection.results.append(hypothesis)

            detection_array.detections.append(detection)

        return detection_array


def main(args=None):
    """Start the YOLOv11 detector node."""
    rclpy.init(args=args)
    node = Yolov11Detector()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
