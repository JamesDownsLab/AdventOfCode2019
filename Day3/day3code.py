# Crossed Wires

import numpy as np

with open('input.txt', 'r') as f:
    input1, input2 = f.readlines()
input1 = input1.split(',')
input2 = input2.split(',')


def get_instructions(input):
    return [(i[0], int(i[1:])) for i in input]

path1 = get_instructions(input1)
path2 = get_instructions(input2)

def get_coords(path):
    points = [(0, 0)]
    for (dir, dist) in path:
        (x, y) = points[-1]
        if dir == 'R':
            points += [(xi, y) for xi in range(x+1, x+1+dist)]
        elif dir == 'L':
            points += [(xi, y) for xi in range(x-1, x-1-dist, -1)]
        elif dir == 'U':
            points += [(x, yi) for yi in range(y+1, y+1+dist)]
        else:
            points += [(x, yi) for yi in range(y-1, y-1-dist, -1)]
    return points

path1points = get_coords(path1)
path2points = get_coords(path2)

a = set(path1points)
b = set(path2points)

crossings = a & b

crossings = np.array(list(crossings))
# manhattan_distance = np.sum(np.abs(crossings), axis=1)

manhattan_distance = [abs(a) + abs(b) for a, b in crossings]
manhattan_distance.sort()
print('\n Closest intersection: ', manhattan_distance[1], '\n')

path1points = np.array(path1points)
path2points = np.array(path2points)
distances = []
for crossing in crossings:
    # print(crossing)
    path1_crossings = (path1points[:, 0] == crossing[0]) * (path1points[:, 1] == crossing[1])
    path2_crossings = (path2points[:, 0] == crossing[0]) * (path2points[:, 1] == crossing[1])
    path1_crossings_distances = np.nonzero(path1_crossings)[0][0]
    path2_crossings_distances = np.nonzero(path2_crossings)[0][0]
    distances.append(path1_crossings_distances+path2_crossings_distances)

print(np.sort(distances))