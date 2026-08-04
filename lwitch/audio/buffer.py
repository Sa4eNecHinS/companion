import queue


class AudioBuffer:
    def __init__(self):
        self.pcm_queue = queue.Queue(maxsize=30)
        self.dropped_chunks = 0

    def push(self, chunk):
        try:
            self.pcm_queue.put_nowait(chunk)
        except queue.Full:
            self.pcm_queue.get_nowait()  # remove the oldest chunk
            self.pcm_queue.put_nowait(chunk)
            self.dropped_chunks += 1

    def pop(self) -> list[int]:
        return self.pcm_queue.get()

    def __len__(self):
        return self.pcm_queue.qsize()
