import intcode
import random
import matplotlib.pyplot as plt
from queue import Queue


class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Corridor:
    def __init__(self, x, y, approach, approach_tile):
        self.x = x
        self.y = y
        # approach is the direction which is approached from
        options = [1, 2, 3, 4]
        self.approach_tile = approach_tile
        self.backtrack = Queue(1)
        self.options = Queue(3)
        if approach == "N":
            backtrack = 1
            options.remove(1)
        elif approach == "S":
            backtrack = 2
            options.remove(2)
        elif approach == "W":
            backtrack = 3
            options.remove(3)
        else:
            backtrack = 4
            options.remove(4)
        self.backtrack.put(backtrack)
        for o in options:
            self.options.put(o)

    def next_move(self):
        if not self.options.empty():
            return self.options.get()
        elif not self.backtrack.empty():
            return self.backtrack.get()
        else:
            return None


class RepairDroid:

    def __init__(self, computer):
        self.computer = computer
        self.corridors = {}
        self.walls = {}

    def map_corridors(self):
        x = 0
        y = 0
        tile = Corridor(x, y, None, None)
        self.corridors[(x, y)] = tile
        mapped = False
        while not mapped:
            next_move = tile.next_move()
            if next_move is None:
                mapped = True
            else:
                self.computer.inputs.append(next_move)
                output = self.computer.run()
                new_x, new_y = self.get_new_xy(next_move, x, y)
                if output == 0:
                    self.walls[(new_x, new_y)] = Wall(new_x, new_y)
                elif output > 0:
                    if (new_x, new_y) not in self.corridors:
                        tile = Corridor(new_x, new_y, self.get_approach(next_move), tile)
                        self.corridors[(new_x, new_y)] = tile
                    else:
                        tile = self.corridors[(new_x, new_y)]
                    if output == 2:
                        oxygen = (new_x, new_y)
                    x = new_x
                    y = new_y
        return oxygen

    def distance_to_oxygen(self, oxygen):
        tile = self.corridors[oxygen]
        distance = 0
        while True:
            distance += 1
            tile = tile.approach_tile
            if tile.x == 0 and tile.y == 0:
                return distance

    def get_new_xy(self, command, x, y):
        new = {1: (x, y + 1), 2: (x, y - 1), 3: (x-1, y), 4: (x+1, y)}
        return new[command]

    def get_approach(self, command):
        approaches = {1: "S", 2: "N", 3: "E", 4: "W"}
        return approaches[command]


def plot_tiles(tiles):
    wall_x = []
    wall_y = []
    for tile in tiles.values():
        wall_x.append(tile.x)
        wall_y.append(tile.y)
    plt.plot(wall_x, wall_y, 'x')
    plt.plot(oxygen[0], oxygen[1], 'o')
    plt.show()

def plot_map(walls, oxygen):
    x, y = zip(*[[w.x, w.y] for w in walls.values()])
    plt.plot(x, y, 'x')
    plt.plot(oxygen[0], oxygen[1], 'o')
    plt.plot(0, 0, '+')
    plt.legend(['Walls', 'oxygen', 'origin'])
    plt.show()




if __name__ == "__main__":
    computer = intcode.IntcodeComputer(intcode.read_intcode_input_file('input.txt'), [])
    repair_droid = RepairDroid(computer)
    oxygen = repair_droid.map_corridors()
    distance = repair_droid.distance_to_oxygen(oxygen)
    print(oxygen)
    print(distance)
    plot_tiles(repair_droid.walls)
