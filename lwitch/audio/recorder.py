from lwitch.audio.buffer import AudioBuffer
from lwitch.audio.resampler import AudioResampler
from lwitch.audio.chunker import AudioChunker
from lwitch.audio.microphone import Microphone


class Recoder:
    def __init__(self, raw_buffer: AudioBuffer, pcm_buffer: AudioBuffer):
        self.raw_buffer = raw_buffer
        self.resampler = AudioResampler()
        self.chunker = AudioChunker()
        self.pcm_buffer = pcm_buffer

        self.mic = Microphone(raw_buffer)

    def start(self):
        print("func start() began working")
        count = 0
        self.mic.start()

        while True:
            print("start() itetation: ", count)

            raw = self.raw_buffer.pop()

            if raw is None:
                break

            print("convert_to_16k")
            pcm = self.resampler.convert_to_16k(raw)
            print("resize chunks")
            chunks = self.chunker.get_chunks(pcm)

            for chunk in chunks:
                print("add chunks to queue")
                self.pcm_buffer.push(chunk)

            count += 1

            if count == 100:
                self.mic.stop()
                print("\n\n PIPILINE stopped")
                break

    def stop(self):
        print("func stop() began working")
        self.raw_buffer.push(None)


if __name__ == "__main__":
    raw_buffer = AudioBuffer()
    pcm_buffer = AudioBuffer()

    recorder = Recoder(raw_buffer, pcm_buffer)

    recorder.start()
