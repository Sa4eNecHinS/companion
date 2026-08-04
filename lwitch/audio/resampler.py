import numpy as np


class AudioResampler:
    def __init__(
        self,
        irate=48_000,
        orate=16_000,
    ):
        self.irate = irate  # input rate
        self.orate = orate  # output rate
        self.ratio = self.irate / self.orate
        self.buffer = []

    def convert_to_16k(self, chunk):
        # common buffer: the part of old buffer + new chunk
        self.buffer.append(chunk)

        # cant use len, cause len([1, [2, 3]]) -> 2
        total_samples = sum(len(c) for c in self.buffer)
        # number of ready output samples from current buffer
        new_len = int(total_samples / self.ratio)

        if new_len == 0:
            return []

        # number of input samples, which will take to work now
        # need cause 'reshape' would raise error
        usable_samples = int(new_len * self.ratio)

        full_data = np.concatenate(self.buffer)
        # taking a whole sample's part
        to_process = full_data[:usable_samples]

        # save sample's remainder for the next buffer
        remainder = full_data[usable_samples:]
        if len(remainder) > 0:
            self.buffer = [remainder]
        else:
            self.buffer = []

        # first: split the whole int sample into parts by int(2.75) = 2,
        # after it meaning every axis
        resampled = to_process.reshape(-1, int(self.ratio)).mean(axis=1)
        return resampled
