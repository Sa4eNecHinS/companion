import numpy as np


class AudioChunker:
    def __init__(self):
        # self.buffer = np.array([], dtype=np.float32)
        self.buffer = []
        self.chunk_size = 480  # freq / time

    def get_chunks(self, chunk):
        # merge old chunk with new one
        self.buffer.append(chunk)

        # how many whole chunks can collect
        total_samples = sum(len(c) for c in self.buffer)

        new_len = int(total_samples / self.chunk_size)

        if new_len == 0:
            return []

        # number of chunks that divide on chunk_size
        usable_samples = int(new_len * self.chunk_size)

        full_data = np.concatenate(self.buffer)

        common_chunk = full_data[:usable_samples]
        # save remainder
        remainder = full_data[usable_samples:]
        if len(remainder) > 0:
            self.buffer = [remainder]
        else:
            self.buffer = []

        # transform to matrix with attached matrixs with chunk_size
        chunk_list = common_chunk.reshape(-1, self.chunk_size)

        return chunk_list
