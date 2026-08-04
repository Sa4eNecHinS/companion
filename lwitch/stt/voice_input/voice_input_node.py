import rclpy
from rclpy.node import Node
from std_msgs.msg import String


from lwitch.stt.record import record
from lwitch.audio.recorder import Recorder
from lwitch.audio.buffer import AudioBuffer


class VoiceInputNode(Node):
    def __init__(self):
        super().__init__("voice_input_node")

        self.publisher_ = self.create_publisher(String, "/voice_input", 10)

        self.raw_buffer = AudioBuffer()
        self.pcm_buffer = AudioBuffer()
        self.recorder = Recorder(self.raw_buffer, self.pcm_buffer)
        # self.duration = 3

    def record_and_publish(self):
        self.get_logger().info("Starting voice recording...")

        self.recorder.start()

        self.get_logger().info("Voice input successfully recorded")

        msg = String()
        msg.data = "voice_recorded"
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = VoiceInputNode()

    try:
        node.record_and_publish()
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nПокедова!\n")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
