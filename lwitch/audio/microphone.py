import sounddevice as sd


class Microphone:
    def __init__(
        self,
        buffer,
        rate=48_000,
        device=None,
        channels=1,
        dtype="float32",
    ):
        self.buffer = buffer
        self.device = device
        self.rate = rate
        self.channels = channels
        self.dtype = dtype

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
