import itertools
import sys


class IntcodeComputer:

    opcode_instructions = {1: 'Add', 2: 'Multiply', 3: 'Input', 4:'Output', 5: 'JumpIfTrue', 6: 'JumpIfFalse',
                       7: 'LessThan', 8: 'Equals', 99: 'Halt'}
    parameter_modes = {0: 'Position', 1: 'Immediate'}

    def __init__(self, intcode, inputs, return_outputs=False):
        self.intcode = intcode
        self.inputs = inputs
        self.inputs_used = 0
        self.return_outputs = return_outputs
        self.i = 0

    def run(self):
        while self.i < len(self.intcode):
            opcode = self.intcode[self.i]
            mode, parameter_modes = self.process_opcode(opcode)
            if mode == 'Halt':
                break
            # print(mode)
            functions = {'Add': self.add,
                         'Multiply': self.multiply,
                         'Input': self.input,
                         'Output': self.output,
                         'JumpIfTrue': self.jumpiftrue,
                         'JumpIfFalse': self.jumpiffalse,
                         'LessThan': self.lessthan,
                         'Equals': self.equal,
                         'Halt': self.halt}

            out = functions[mode](parameter_modes)
            if out is not None:
                return out

    def add(self, modes):
        first = self.get_parameter(self.i+1, modes[0])
        second = self.get_parameter(self.i+2, modes[1])
        pos = self.get_parameter(self.i+3, 'Immediate')
        self.intcode[pos] = first + second
        self.i += 4

    def multiply(self, modes):
        first = self.get_parameter(self.i + 1, modes[0])
        second = self.get_parameter(self.i + 2, modes[1])
        pos = self.get_parameter(self.i + 3, 'Immediate')
        self.intcode[pos] = first * second
        self.i += 4

    def input(self, modes):
        pos = self.get_parameter(self.i+1, 'Immediate')
        input_value = self.get_next_input()
        self.intcode[pos] = input_value
        self.i += 2

    def output(self, modes):
        output = self.get_parameter(self.i+1, modes[0])
        self.i += 2
        return output

    def jumpiftrue(self, modes):
        first = self.get_parameter(self.i+1, modes[0])
        second = self.get_parameter(self.i+2, modes[1])
        if first != 0:
            self.i = second
        else:
            self.i += 3

    def jumpiffalse(self, modes):
        first = self.get_parameter(self.i + 1, modes[0])
        second = self.get_parameter(self.i + 2, modes[1])
        if first == 0:
            self.i = second
        else:
            self.i += 3

    def lessthan(self, modes):
        first = self.get_parameter(self.i+1, modes[0])
        second = self.get_parameter(self.i+2, modes[1])
        pos = self.get_parameter(self.i+3, 'Immediate')
        self.intcode[pos] = 1 if first < second else 0
        self.i += 4

    def equal(self, modes):
        first = self.get_parameter(self.i+1, modes[0])
        second = self.get_parameter(self.i+2, modes[1])
        pos = self.get_parameter(self.i+3, 'Immediate')
        self.intcode[pos] = 1 if first == second else 0
        self.i += 4

    def halt(self, modes):
        return 'HALT'

    def get_next_input(self):
        if self.inputs_used >= len(self.inputs):
            input_value = int(input('Enter an integer input : '))
        else:
            input_value = self.inputs[self.inputs_used]
        self.inputs_used += 1
        return input_value

    def get_parameter(self, pos, mode):
        return self.intcode[self.intcode[pos]] if mode == 'Position' else self.intcode[pos]

    def process_opcode(self, opcode):
        opcode = str(opcode)
        mode = opcode[-2:]
        p_modes = []
        for p in range(3, 6):
            if p <= len(opcode):
                p_modes.append(int(opcode[-p]))
            else:
                p_modes.append(0)
        return self.opcode_instructions[int(mode)], [self.parameter_modes[p] for p in p_modes]


def read_intcode_input_file(file):
    with open(file, 'r') as f:
        file = f.read()
    intcode = file.split(',')
    intcode = [int(i) for i in intcode]
    return intcode

def convert_string_to_intcode(intcode_string):
    intcode = intcode_string.split(',')
    intcode = [int(i) for i in intcode]
    return intcode

def test():
    intcode = convert_string_to_intcode("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
    input_codes = [1, 0, 4, 3, 2]
    output = run_amp_circuit(intcode, input_codes)
    if output == 65210:
        return True
    else:
        return False

def run_amp_circuit(intcode, inputs):
    output = 0
    for input_code in inputs:
        computer = IntcodeComputer(intcode, [input_code, output], return_outputs=True)
        output = computer.run()
    return output

def run_part_1():
    intcode = read_intcode_input_file('input.txt')
    input_codes = [0, 1, 2, 3, 4]
    input_iterations = itertools.permutations(input_codes)
    outputs = []
    for iteration in input_iterations:
        # print(iteration)
        output = run_amp_circuit([i for i in intcode], iteration)
        outputs.append(output)

    print(max(outputs))

def run_part_2():
    intcode = read_intcode_input_file('input.txt')
    input_codes = [9, 8, 7, 6, 5]
    input_iterations = itertools.permutations(input_codes)
    outputs = []
    for iteration in input_iterations:
        computers = []
        output = 0
        for i, input_code in enumerate(iteration):
            computers.append(IntcodeComputer([i for i in intcode], [input_code, output], return_outputs=True))
            output = computers[i].run()
        finished = False
        while not finished:
            for i in range(5):
                computers[i].inputs += [output]
                out = computers[i].run()
                if out is None:
                    finished = True
                    break
                else:
                    output = out
        print(output)
        outputs.append(output)
    print('Max : ', max(outputs))



if __name__ == "__main__":
    test_result = test()
    if test_result:
        print('Test passed')
    else:
        print('Test Failed')
        sys.exit()
    run_part_1()
    run_part_2()
