#!/usr/bin/env python3
print("Imports...")
import os
import rclpy
import cv2
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from ament_index_python.packages import get_package_share_directory
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from image_segmentation import ImageSegmentation
from white_blob_detect import BlobDetect
print("Imports...Done")

class ImageListener(Node):
    def __init__(self, name_topic="/image_raw", timer_period=5.0, object_name=""):
        super().__init__('image_listener')
        self._object_name = object_name

        self.init_ai_models()
        self.package_path = get_package_share_directory("vision_unit_pkg")
        self.bridge = CvBridge()

        self.create_subscription(
            Image,
            name_topic,
            self.listener_callback,
            10,
            callback_group=MutuallyExclusiveCallbackGroup()
        )
        self.init_image_var()
        self.timer = self.create_timer(
            timer_period, self.timer_callback, callback_group=MutuallyExclusiveCallbackGroup())

    def init_ai_models(self):
        self.get_logger().warning("Loading Models AI..")
        self.i_segment = ImageSegmentation()
        self.blob= BlobDetect(False)
        self.get_logger().warning("Loading Models AI..DONE")

    def init_image_var(self):
        img_path = os.path.join(self.package_path, "scripts/init_image/deepmindbot.png")
        self.cv_image = cv2.imread(img_path)

        if self.cv_image is None:
            self.get_logger().error(f"Error loading image={img_path}")
            assert False, "Something went wrong in init image"

        cv2.imshow('Camera Image', self.cv_image)
        cv2.waitKey(1)

    def listener_callback(self, img_msg):
        self.cv_image = self.bridge.imgmsg_to_cv2(img_msg, desired_encoding='bgr8')

    def timer_callback(self):
        object_list = [self._object_name]

        # Resize the image to be 4 times smaller
        new_width = int(self.cv_image.shape[1] / 2)
        new_height = int(self.cv_image.shape[0] / 2)
        resized_image = cv2.resize(self.cv_image, (new_width, new_height))

        # Send the resized image to the segmentation function
        seg_image = self.i_segment.generate_image_segmentation(resized_image, object_list, False)
        result, mark_image = self.blob.detect_large_white_blob(seg_image)
        print("Found person?="+str(result))

        cv2.imshow('Camera Image', mark_image)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    image_listener = ImageListener(name_topic="/wrist_rgbd_depth_sensor/image_raw", timer_period=0.5, object_name="person")
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(image_listener)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        image_listener.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
