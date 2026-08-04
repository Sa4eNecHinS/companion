import rclpy

from rclpy.node import Node
from std_msgs.msg import String

from lwitch.llm.llm_client import ask_llm
from lwitch.waf.security.sql_detector import detect_sql_injection
from lwitch.waf.security.sanitizer import sanitize_input
from lwitch.waf.security.rate_limiter import RateLimiter
from lwitch.waf.utils.logger_config import setup_file_logger
from lwitch.waf.database.crud import create_dialogue


class WafFilterNode(Node):
    def __init__(self):
        super().__init__("waf_filter_node")

        # type message - String
        # topic name - /voice_input
        # queue size - 10
        self.subscription = self.create_subscription(
            String, "/stt_output", self.message_callback, 10
        )

        self.publisher_ = self.create_publisher(String, "/waf_output", 10)
        self.file_logger = setup_file_logger("waf_filter_node")
        self.rate_limiter = RateLimiter()

        self.log_info("WAF filter started")

    def log_info(self, message):
        self.get_logger().info(message)
        self.file_logger.info(message)

    def log_warning(self, message):
        self.get_logger().warning(message)
        self.file_logger.warning(message)

    def message_callback(self, msg):
        user_input = msg.data

        if self.rate_limiter.allow():
            self.log_info(f'Received: "{user_input}"')

            detected_pattern = detect_sql_injection(user_input)
            if detected_pattern:
                self.log_warning(
                    f"BLOCKED: SQL Injection detected | Pattern: {detected_pattern}"
                )
                create_dialogue(
                    timestamp=str(self.rate_limiter.get_status()[0]),
                    user_id="default_user",
                    user_input=user_input,
                    sanitized_user_input=None,
                    is_blocked=True,
                    block_reason=detected_pattern,
                    llm_response=None,
                )
                return None

            sanitized_input, changes = sanitize_input(user_input)

            # проверка очищенного текста
            normalized_detected = detect_sql_injection(sanitized_input)
            if normalized_detected:
                self.log_warning(
                    f"BLOCKED NORMALIZED SQLi | Pattern: {normalized_detected}"
                )
                return None

            if changes:
                self.log_info(f"Input sanitized | Changes: {', '.join(changes)}")

            llm_response = ask_llm(sanitized_input)

            clean_msg = String()  # т.к publish ожидает String из msg

            if llm_response:
                clean_msg.data = sanitized_input + "\n" + llm_response
            else:
                clean_msg.data = sanitized_input

            create_dialogue(
                timestamp=str(self.rate_limiter.get_status()[0]),
                user_id="default_user",
                user_input=user_input,
                sanitized_user_input=sanitized_input,
                is_blocked=False,
                block_reason=None,
                llm_response=llm_response,
            )

            self.publisher_.publish(clean_msg)
            self.log_info(f'PASSED: "{clean_msg.data}"')
        else:
            self.log_info(
                f"Too many requests. Max req/min = {self.rate_limiter.max_requests}"
            )


def main(args=None):
    rclpy.init(args=args)

    node = WafFilterNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.log_info("\nПокедова от WAF!\n")

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
