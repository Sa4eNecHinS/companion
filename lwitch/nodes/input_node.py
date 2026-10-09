import rclpy

from rclpy.node import Node
from std_msgs.msg import String

from lwitch.waf.utils.logger_config import setup_file_logger
from lwitch.waf.security.sanitizer import safe_text


class InputNode(Node):
    def __init__(self):
        super().__init__("input_node")

        self.publisher_ = self.create_publisher(String, "/stt_output", 10)
        self.file_logger = setup_file_logger("input_node")

        self.get_logger().info("Input node started")
        self.file_logger.info("Input node started")

    def run(self):
        while rclpy.ok():
            user_input = input("You > ")
            safe_input = safe_text(user_input)

            if safe_input != user_input:
                self.get_logger().info("Invalid unicode character were removed")

            msg = String()
            msg.data = safe_input

            self.publisher_.publish(msg)
            self.get_logger().info(f'Published: "{user_input}"')


def main(args=None):
    rclpy.init(args=args)
    node = InputNode()

    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info("\nПокедова!\n")
        node.file_logger.info("\nПокедова!\n")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
