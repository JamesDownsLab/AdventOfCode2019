# Flawed Frequency Transmission
import numpy as np
from tqdm import tqdm

class FFTMachine:

    def __init__(self):
        self.base = [0, 1, 0, -1]

    def run(self, signal, phases):
        for p in tqdm(range(phases)):
            signal = self.apply(signal)
        return signal

    def apply(self, signal):
        result = []
        for r in range(len(signal)):
            pattern = self.pattern(r, len(signal))
            result.append(sum([s*p for s, p in zip(signal, pattern)]))
        return [abs(r) % 10 for r in result]

    def pattern(self, r, length):
        pattern = [i for b in self.base for i in [b]*(r+1)]
        return (pattern * (length//len(pattern) + 1))[1:length+1]

class Paul2718sFFTMachine:
    # output at N is sum of all the digits between N and the end for N > len(signal)/2
    # Uses ideas from reddit user /u/paul2718

    def __init__(self):
        pass

    def run(self, signal, phases):
        signal = np.flip(signal)
        for p in tqdm(range(phases)):
            signal = self.apply(signal)
        return np.flip(signal)

    def apply(self, signal):
        signal = np.cumsum(signal)
        signal = np.abs(signal) % 10
        return signal




if __name__ == "__main__":

    ## Part 1
    with open('input.txt', 'r') as f:
        signal = [int(s) for s in f.read() if s != "\n"]
    fft_machine = FFTMachine()
    signal = fft_machine.run(signal, 100)
    print("Part one result: ", signal[:8])


    ## Part 2
    # with open('input.txt', 'r') as f:
    #     signal = [int(s) for s in f.read() if s != "\n"]*10000
    # start = ""
    # for s in range(7):
    #     start += str(signal[s])
    # print(start)
    # start = int(signal)
    # fft_machine = Paul2718sFFTMachine()
    # signal = fft_machine.run(signal, 100)
    # print("Part two result: ", signal[start:start+8])

