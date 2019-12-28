import intcode
import matplotlib.pyplot as plt
from queue import Queue


class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Corridor:
    def __init__(self, x, y, approach):
        self.x = x
        self.y = y
        # approach is the direction which is approached from
        options = [1, 2, 3, 4]
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
        tile = Corridor(x, y, None)
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
                        tile = Corridor(new_x, new_y, self.get_approach(next_move))
                        self.corridors[(new_x, new_y)] = tile
                    else:
                        tile = self.corridors[(new_x, new_y)]
                    if output == 2:
                        oxygen = (new_x, new_y)
                    x = new_x
                    y = new_y
        return oxygen

    def path_to_oxygen(self, oxygen):
        paths = self.graph.find_all_paths(oxygen, (0, 0))
        path_lengths = [len(p) for p in paths]
        shortest = min(path_lengths)
        for path, length in zip(paths, path_lengths):
            if length == shortest:
                return path

    def get_new_xy(self, command, x, y):
        new = {1: (x, y + 1), 2: (x, y - 1), 3: (x-1, y), 4: (x+1, y)}
        return new[command]

    def get_approach(self, command):
        approaches = {1: "S", 2: "N", 3: "E", 4: "W"}
        return approaches[command]

    def generate_graph(self, oxygen):
        graph = {}
        tile = self.corridors[oxygen]
        tiles_to_graph = Queue()
        tiles_to_graph.put(tile)
        while not tiles_to_graph.empty():
            tile = tiles_to_graph.get()
            adjacent_tiles = self.adjacent_tiles(tile)
            if (tile.x, tile.y) not in graph.keys():
                graph[(tile.x, tile.y)] = [(t.x, t.y) for t in adjacent_tiles]
                for t in adjacent_tiles:
                    tiles_to_graph.put(t)
        self.graph = Graph(graph)
        return self.graph

    def adjacent_tiles(self, tile):
        x, y = tile.x, tile.y
        tiles = []
        possible_keys = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for key in possible_keys:
            if key in self.corridors.keys():
                tiles.append(self.corridors[key])
        return tiles

    def fill_oxygen(self, oxygen):
        # find the distance between all tiles and oxygen
        furthest = 0
        tile = self.corridors[oxygen]
        other_tiles = [c for key, c in self.corridors.items() if key != oxygen]
        for t in other_tiles:
            paths = self.graph.find_all_paths((tile.x, tile.y), (t.x, t.y))
            length = min([len(p) for p in paths])
            if length > furthest:
                furthest = length
        return furthest


def plot_map(walls, oxygen, path):
    x, y = zip(*[[w.x, w.y] for w in walls.values()])
    plt.plot(x, y, 'x')
    plt.plot(oxygen[0], oxygen[1], 'o')
    plt.plot(0, 0, '+')
    pathx, pathy = zip(*path)
    plt.plot(pathx, pathy)
    plt.legend(['Walls', 'oxygen', 'origin', 'path'])
    plt.show()


class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to
            end_vertex in graph """
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        return paths



if __name__ == "__main__":
    computer = intcode.IntcodeComputer(intcode.read_intcode_input_file('input.txt'), [])
    repair_droid = RepairDroid(computer)
    oxygen = repair_droid.map_corridors()
    repair_droid.generate_graph(oxygen)
    path_to_oxygen = repair_droid.path_to_oxygen(oxygen)
    print("Distance to oxygen = ", len(path_to_oxygen)-1)
    minutes = repair_droid.fill_oxygen(oxygen) - 1
    print("mintutes to fill oxygen : ", minutes)
    plot_map(repair_droid.walls, oxygen, path_to_oxygen)