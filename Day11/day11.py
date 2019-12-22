import intcode
import numpy as np
import matplotlib.pyplot as plt

BLACK = 0
WHITE = 1


class Hull:

    def __init__(self, w):
        self.w = w
        self.panels = {}
        for x in range(-w, w):
            for y in range(-w, w):
                self.panels[(x, y)] = Panel(x, y)

    def show_hull(self):
        im = np.zeros((2*self.w, 2*self.w))
        for key, panel in self.panels.items():
            x, y = key
            x += self.w
            y += self.w
            im[y, x] = panel.color
        plt.imshow(im)
        plt.show()


class Panel:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = BLACK
        self.times_painted = 0

    def paint(self, color):
        self.color = color
        self.times_painted += 1


class Robot:

    def __init__(self, hull, program, start_on_white=False):
        self.hull = hull
        self.x = 0
        self.y = 0
        if start_on_white:
            self.hull.panels[(0, 0)].color = WHITE
        self.direction = 'Up'
        self.brain = intcode.IntcodeComputer(program, [])

    def run(self):
        finished = False
        while not finished:
            current_panel = self.hull.panels[(self.x, self.y)]
            current_color = current_panel.color
            self.brain.add_inputs(current_color)
            new_color = self.brain.run()
            turn_direction = self.brain.run()
            if new_color is None:
                finished = True
                break
            current_panel.paint(new_color)
            self.set_new_direction(turn_direction)
            self.move()

    def move(self):
        if self.direction == 'Up':
            self.y += 1
        elif self.direction == 'Right':
            self.x += 1
        elif self.direction == 'Down':
            self.y -= 1
        else:
            self.x -= 1

    def set_new_direction(self, dir):
        if self.direction == 'Up':
            self.direction = 'Left' if dir == 0 else 'Right'
        elif self.direction == 'Right':
            self.direction = 'Up' if dir == 0 else 'Down'
        elif self.direction == 'Down':
            self.direction = 'Right' if dir == 0 else 'Left'
        else:
            self.direction = 'Down' if dir == 0 else 'Up'


if __name__ == "__main__":
    program = intcode.read_intcode_input_file('input.txt')
    hull = Hull(100)
    robot = Robot(hull, program, start_on_white=True)
    robot.run()
    painted = 0
    for panel in hull.panels.values():
        if panel.times_painted > 0:
            painted += 1
    print(painted)
    hull.show_hull()

