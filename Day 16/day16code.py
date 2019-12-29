# Flawed Frequency Transmission
import numpy as np
from tqdm import tqdm

class FFTMachine:

    def __init__(self):
        self.base = [0, 1, 0, -1]

    def run(self, signal, phases):
        for p in tqdm(range(phases)):
            signal = self.apply(signal)
            print(signal)
        return signal

    def apply(self, signal):
        result = []
        for r in range(len(signal)):
            pattern = self.pattern(r, len(signal))
            step = 0
            for s, p in zip(signal, pattern):
                step += s * p
            result.append(int(str(step)[-1]))
        return result

    def pattern(self, r, length):
        r += 1
        pattern = [[b]*r for b in self.base]
        pattern = [item for sublist in pattern for item in sublist]
        return [pattern[(l+len(pattern))%len(pattern)] for l in range(1, length+1)]

class FFTMachineWithNumpy:

    def __init__(self):
        self.base = np.array([0, 1, 0, -1])

    def run(self, signal, phases):
        pattern = self.pattern(len(signal))
        for p in range(phases):
            signal = self.apply(signal)
        return signal

    def apply(self, signal):
        pattern = self.pattern(len(signal))
        out = signal * pattern
        out = out.sum(axis=1)
        return [int(str(o)[-1]) for o in out]

    def pattern(self, length):
        pattern = np.zeros((length, length), dtype=np.int16)
        for r in range(length):
            pattern[r, :] = np.resize(np.repeat(self.base, r+1), length+1)[1:]
        return pattern

class FFTMachineNumpy:

    def __init__(self):
        self.base = np.array([0, 1, 0, -1])

    def run(self, signal, phases):
        for p in tqdm(range(phases)):
            signal = self.apply(signal)
        return signal

    def apply(self, signal):
        result = []
        for r in range(len(signal)):
            pattern = self.pattern(r, len(signal))
            result.append(int(str(np.sum(pattern*signal))[-1]))
        return np.array(result)

    def pattern(self, r, length):
        return np.resize(np.repeat(self.base, r+1), length+1)[1:]


class Paul2718sFFTMachine:
    # output at N is sum of all the digits between N and the end for N > len(signal)/2
    def __init__(self):
        pass

    def run(self, signal, phases):
        signal = np.flip(signal)
        for p in tqdm(range(phases)):
            signal = self.apply(signal)
        return np.flip(signal)

    # def apply(self, signal):
    #     out = []
    #     for s in range(len(signal)):
    #         part = np.sum(signal[s:])
    #         out.append(int(str(int(part))[-1]))
    #     return out

    def apply(self, signal):
        # signal = np.flip(signal)
        signal = np.cumsum(signal)
        signal = np.abs(signal) % 10
        # signal = np.flip(signal)
        return signal




if __name__ == "__main__":
    # signal = [1, 2, 3, 4, 5, 6, 7, 8]
    # signal = [int(s) for s in "80871224585914546619083218645595"]
    with open('input.txt', 'r') as f:
        signal = [int(s) for s in f.read() if s != "\n"]*10000
    # print(len(signal))
    start = ""
    for s in range(7):
        start += str(signal[s])
    start = int(start)
    print(start)
    # fft_machine = FFTMachine()
    # fft_machine = FFTMachineNumpy()
    fft_machine = Paul2718sFFTMachine()
    signal = fft_machine.run(signal, 100)
    print(signal)
    print(signal[start:start+10])

