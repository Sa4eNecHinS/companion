import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from lwitch.srv import CheckSafety

from lwitch.stt.stt import speak_to_text
from lwitch.llm.llm_client import ask_llm


class SttNode(Node):
    def __init__(self):
        super().__init__("stt_node")
        self.publisher_ = self.create_publisher(
            String,  # тип передоваемых сообщений
            "/stt_output",  # название топика
            10,  # размер очереди
        )

        self.path = "src/lwitch/lwitch/stt/record.wav"
        self.is_recording = False
        self.duration = 3  # secs

        self.srv_ = self.create_service(
            CheckSafety,
            "CheckSafety",
            self.check_safety,
        )

        # self.subscriber_ = self.create_subscription(
        #    String, "/voice_input", self.translate_speak, 10
        # )

    def log_info(self, message):
        self.get_logger().info(message)
        # self.file_logger.info(message)

    def log_warning(self, message):
        self.get_logger().warning(message)
        # self.file_logger.warning(message)

    def check_safety(self, request, response):
        safe = request.input_text

    def translate_speak(self):
        msg = String()
        self.log_info("Start analize ur speak ...")

        info = speak_to_text(self.path)
        msg.data = info.get("text", None)

        if not msg.data:
            self.log_warning("The voice input is empty")

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

        response = ask_llm(user_input=info.get("text", None))
        if not response:
            self.log_info("LLM didnt response")
            return

        self.log_info(f"LLM: {response}")


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
