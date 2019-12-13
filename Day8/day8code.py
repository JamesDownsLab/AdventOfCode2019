with open('input.txt', 'r') as f:
    image_data = f.read()

# print(image_data)

width = 25
height = 6

elements_per_im = width * height

class Layer:
    def __init__(self, data, layer_no):
        self.layer = [int(l) for l in data if l != '\n']
        self.layer_no = layer_no
        self.counts = {}
        self.counts[0] = len([i for i in self.layer if i == 0])
        self.counts[1] = len([i for i in self.layer if i == 1])
        self.counts[2] = len([i for i in self.layer if i == 2])

    def pixel(self, r, c):
        # print((r+c+2*r))
        return self.layer[r+c+(width-1)*r]


layers = []
for layer_no, i in enumerate(range(0, len(image_data)-1, elements_per_im)):
    layer = image_data[i:i+elements_per_im]
    layers.append(Layer(layer, layer_no))

zeros = [l.counts[0] for l in layers]
layer_with_least_zeros = zeros.index(min(zeros))
layer = layers[layer_with_least_zeros]
print(layer.counts[1] * layer.counts[2])

final_im = []
for r in range(height):
    for c in range(width):
        pixels = [l.pixel(r, c) for l in layers]
        for p in pixels:
            if p == 0:
                final_im.append(p)
                break
            elif p == 1:
                final_im.append(p)
                break

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

im = np.array(final_im).reshape(height, width)*255
plt.imshow(im)
plt.show()
print(im)
# im = Image.fromarray(im).show()

