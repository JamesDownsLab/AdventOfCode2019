import intcode

class Tile:

    def __init__(self, x, y, tile_id):
        self.x = x
        self.y = y
        self.tile_id = tile_id


class Game:

    def __init__(self, program):
        self.program = program
        self.computer = intcode.IntcodeComputer(program, [], input_function=self.next_input)
        self.tiles = {}

    def start(self):
        finished = False
        while not finished:
            outputs = [self.computer.run() for i in range(3)]
            if None not in outputs:
                self.parse_outputs(outputs)
            else:
                finished = True
                print(outputs)

    def parse_outputs(self, outputs):
        if (outputs[0] == -1)*(outputs[1] == 0):
            self.score = outputs[2]
            print("Score: ", self.score)
        else:
            if (outputs[0], outputs[1]) not in self.tiles.keys():
                self.tiles[(outputs[0], outputs[1])] = Tile(*outputs)
            else:
                self.tiles[(outputs[0], outputs[1])].tile_id = outputs[2]
            if outputs[2] == 3:
                self.paddle = self.tiles[(outputs[0], outputs[1])]
            elif outputs[2] == 4:
                self.ball = self.tiles[(outputs[0], outputs[1])]


    def block_tiles(self):
        count = 0
        for tile in self.tiles.values():
            if tile.tile_id == 2:
                count += 1
        return count

    def next_input(self):
        try:
            if self.paddle.x < self.ball.x:
                instruction = 1
            elif self.paddle.x > self.ball.x:
                instruction = -1
            else:
                instruction = 0
        except:
            instruction = 0
        return instruction

if __name__ == "__main__":
    program = intcode.read_intcode_input_file('input.txt')
    program[0] = 2
    game = Game(program)
    game.start()
    print(game.block_tiles())
    print(game.score)

