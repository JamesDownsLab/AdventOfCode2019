# Flawed Frequency Transmission

BASE = [0, 1, 0, -1]

class FFTMachine:

    def __init__(self):
        self.base = [0, 1, 0, -1]

    def run(self, signal, phases):
        for p in range(phases):
            signal = self.apply(signal)
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

if __name__ == "__main__":
    # signal = [1, 2, 3, 4, 5, 6, 7, 8]
    # signal = [int(s) for s in "80871224585914546619083218645595"]
    with open('input.txt', 'r') as f:
        signal = [int(s) for s in f.read() if s != "\n"]
    print(signal)
    fft_machine = FFTMachine()
    signal = fft_machine.run(signal, 100)
    print(signal)
