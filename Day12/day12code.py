import itertools
# from numba import jit

class Moon:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = 0, 0, 0

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.vx) + abs(self.vy) + abs(self.vz))

    def __str__(self):
        return "Moon at {}, {}, {} with velocity {}, {}, {}".format(self.x, self.y, self.z, self.vx, self.vy, self.vz)


class System:
    def __init__(self, moons):
        self.moons = moons
        self.initial = [(a.x, a.y, a.z, a.vx, a.vy, a.vz) for a in self.moons]

    def calculate_energy(self):
        total_energy = 0
        for moon in self.moons:
            total_energy += moon.energy()
        print(total_energy)

    def run(self, steps=10):
        for step in range(steps):
            self.calculate_velocities()
            self.update_positions()

    def run_until_same(self):
        finished = False
        steps = 0
        while not finished:
            steps += 1
            print(steps)
            self.calculate_velocities()
            self.update_positions()
            finished = self.check_same()

    def check_same(self):
        current = [(a.x, a.y, a.z, a.vx, a.vy, a.vz) for a in self.moons]
        if current == self.initial:
            return True
        else:
            return False

    def update_positions(self):
        for moon in self.moons:
            moon.update_position()

    def calculate_velocities(self):
        moon_pairs = itertools.combinations(self.moons, 2)
        for moon1, moon2 in moon_pairs:
            x1, x2 = moon1.x, moon2.x
            if x2 > x1:
                moon2.vx -= 1
                moon1.vx += 1
            elif x2 < x1:
                moon2.vx += 1
                moon1.vx -= 1
            y1, y2 = moon1.y, moon2.y
            if y2 > y1:
                moon2.vy -= 1
                moon1.vy += 1
            elif y2 < y1:
                moon2.vy += 1
                moon1.vy -= 1
            z1, z2 = moon1.z, moon2.z
            if z2 > z1:
                moon2.vz -= 1
                moon1.vz += 1
            elif z2 < z1:
                moon2.vz += 1
                moon1.vz -= 1


TEST_MOONS = [
    Moon(-1, 0, 2),
    Moon(2, -10, -7),
    Moon(4, -8, 8),
    Moon(3, 5, -1)
]


def read_input(file):
    with open(file, 'r') as f:
        moon_locations = f.read().splitlines(False)
    moons = []
    for moon_location in moon_locations:
        loc = moon_location[1:-1].split(', ')
        x = int(loc[0].split('=')[1])
        y = int(loc[1].split('=')[1])
        z = int(loc[2].split('=')[1])
        moons.append(Moon(x, y, z))
    return moons

if __name__ == "__main__":
    moons = read_input('input.txt')
    # moons = TEST_MOONS
    system = System(moons)
    # system.run(steps=10000)
    # for moon in moons:
    #     print(moon)
    # system.calculate_energy()
    system.run_until_same()