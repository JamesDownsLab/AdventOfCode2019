import math


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coord = (self.x, self.y)

    def angle(self, a):
        return math.atan2(a.y-self.y, a.x-self.x)
        # return math.atan2(self.x-a.x, self.y-a.y)

    def angles(self, asts):
        return [self.angle(a) for a in asts]

    def distance(self, ast):
        return math.sqrt((ast.y-self.y)**2 + (ast.x-self.x)**2)

    def visibility(self, asteroids):
        angles = [self.angle(a) for a in asteroids]
        dists = [self.distance(a) for a in asteroids]
        unique_angles = set(angles)
        self.visible_asteroids = []
        for angle in unique_angles:
            dists_to_query = [dists[i] for i, ang in enumerate(angles) if ang == angle]
            min_dist = min(dists_to_query)
            visible = [ast for ast, ang, d in zip(asteroids, angles, dists)
                       if (ang == angle)*(d == min_dist)]
            self.visible_asteroids.append(visible[0])
        self.visible = len(self.visible_asteroids)


    def __str__(self):
        return "Asteroid at coordinate {}, {}".format(self.x, self.y)


class AsteroidMap:

    def __init__(self, asteroid_map):
        self.asteroids = []
        self.add_asteroids(asteroid_map)

    def add_asteroids(self, asteroid_map):
        for y, row in enumerate(asteroid_map):
            for x, column in enumerate(row):
                if column == '#':
                    self.asteroids.append(Asteroid(x, y))
                if column == 'X':
                    a = Asteroid(x, y)
                    self.asteroids.append(a)
                    self.station = a

    def query_visibility(self):
        self.add_visibility()
        vis = [a.visible for a in self.asteroids]
        return self.asteroids[vis.index(max(vis))]

    def add_visibility(self):
        for a in self.asteroids:
            a.visibility([ast for ast in self.asteroids if ast != a])

    def destroy_from(self, station):
        destroyed = 0
        asteroids = self.asteroids
        asteroids.remove(station)
        finished = False
        while not finished:
            station.visibility(asteroids)
            angles = station.angles(station.visible_asteroids)
            x = [a.x for a in asteroids]
            y = [a.y for a in asteroids]
            angles = [a + math.pi/2 for a in angles]
            angles = [a + math.pi*2 if a < 0 else a for a in angles]

            ang_sort = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(angles))]
            visible_asteroids = [station.visible_asteroids[i] for i in ang_sort]
            for a in visible_asteroids:
                destroyed += 1
                if destroyed == 200:
                    # plt.plot(x, y)
                    # plt.show()
                    return a
                asteroids.remove(a)
            if len(asteroids) == 0:
                finished = True

def read_input(file):
    with open(file, 'r') as f:
        asteroid_map = f.readlines()
        return asteroid_map

if __name__ == "__main__":
    # asteroid_map = AsteroidMap([
    #  ".#....#####...#..",
    #  "##...##.#####..##",
    #  "##...#...#.#####.",
    #  "..#.....X...###..",
    #  "..#.#.....#....##"]
    # )
    asteroid_map = AsteroidMap(read_input('input.txt'))
    station = asteroid_map.query_visibility()
    # print(station)
    # print(asteroid_map.station)
    last = asteroid_map.destroy_from(station)
    print(last)