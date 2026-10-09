import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from lwitch.stt.stt import speak_to_text


class SttNode(Node):
    def __init__(self):
        super().__init__("stt_node")
        self.publisher_ = self.create_publisher(
            String,  # тип передоваемых сообщений
            "/stt_output",  # название топика
            10,  # размер очереди
        )

        self.declare_parameter("audio_path", "data/record.wav")
        self.path = self.get_parameter("audio_path").value

    def log_info(self, message):
        self.get_logger().info(message)
        # self.file_logger.info(message)

    def log_warning(self, message):
        self.get_logger().warning(message)
        # self.file_logger.warning(message)

    def translate_speak(self):
        msg = String()
        self.log_info("Start analize ur speak ...")

        info = speak_to_text(self.path)
        msg.data = info.get("text", None)

        if not msg.data:
            self.log_warning("The voice input is empty")
            return

        self.publisher_.publish(msg)
        self.log_info(
            f"""Detected language {info.get("language", None)} with probability {
                info.get("language_probability", None)
            }"""
        )
        self.log_info(
            f"""[{info.get("start_record", None)} -> {info.get("end_record", None)}]: {
                msg.data
            }\n"""
        )


def main(args=None):
    rclpy.init(args=args)
    node = SttNode()

    try:
        node.translate_speak()
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nПокедова!\n")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
