
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.timer_ = self.create_timer(0.1, self.timer_callback)
        self.cap_ = cv2.VideoCapture(0)  # Open default webcam. CHANGE THIS if index 0 does not work for you. (e.g., 1/2/3/4)
        self.bridge_ = CvBridge()
        self.get_logger().info('Camera Node has been started!')

    def timer_callback(self):
        ret, frame = self.cap_.read()
        if ret:
            # To convert OpenCV image to ROS 2 Image message
            img_msg = self.bridge_.cv2_to_imgmsg(frame, encoding = "bgr8")
            self.publisher_.publish(img_msg)
            
            # This displays it locally by using OpenCV just to verify it works
            cv2.imshow("Camera Feed", frame)
            cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.cap_.release()
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
