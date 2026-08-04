import threading
import sounddevice as sd

# from lwitch.log.logger import Logger


class Microphone:
    def __init__(
        self,
        buffer,
        rate=48_000,
        device="Fifine Microphone Mono",
        channels=1,
        dtype="float32",
    ):
        self.buffer = buffer
        self.device = device
        self.rate = rate
        self.channels = channels
        self.dtype = dtype

        # self.logger = Logger(__name__)
        self.stream = None

    def start(self):
        if self.stream is not None:
            return

        self.stream = sd.InputStream(
            samplerate=self.rate,
            channels=self.channels,
            dtype=self.dtype,
            device=self.device,
            callback=self._callback,
        )
        self.stream.start()
        print("stream started")

    def stop(self):
        if self.stream is None:
            return

        self.stream.stop()
        self.stream.close()
        self.stream = None
        print("stream closed")

    def _callback(self, indata, frames, time, status):
        # indata.copy() - cause, sounddevice keep audio chunks at one
        # memory location, which means new rewrite old one, and at the end
        # without .copy in queue were only the new chunks
        self.buffer.push(indata.copy())


if __name__ == "__main__":
    from lwitch.audio.buffer import AudioBuffer

    buf = AudioBuffer()
    mic = Microphone(buf)
    print("\nstart recording: ")
    mic.microphone_recording()

    print("queue size: ", len(buf))
    print("dropped chunks: ", buf.dropped_chunks)
