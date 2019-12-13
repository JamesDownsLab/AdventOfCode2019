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

    def process_code(self):
        i = 0
        while i < len(self.intcode):
            opcode = self.intcode[i]
            mode, parameter_modes = self.process_opcode(opcode)
            if mode == 'Add':
                first = self.get_parameter(i+1, parameter_modes[0])
                second = self.get_parameter(i+2, parameter_modes[1])
                pos = self.get_parameter(i+3, 'Immediate')
                self.intcode[pos] = first + second
                i += 4

            elif mode == 'Multiply':
                first = self.get_parameter(i + 1, parameter_modes[0])
                second = self.get_parameter(i + 2, parameter_modes[1])
                pos = self.get_parameter(i + 3, 'Immediate')
                self.intcode[pos] = first * second
                i += 4

            elif mode == 'Input':
                pos = self.get_parameter(i+1, 'Immediate')
                input_value = self.get_next_input()
                self.intcode[pos] = input_value
                i += 2

            elif mode == 'Output':
                output = self.get_parameter(i+1, parameter_modes[0])
                if self.return_outputs:
                    return output
                else:
                    print(output)
                i += 2

            elif mode == 'JumpIfTrue':
                first = self.get_parameter(i+1, parameter_modes[0])
                second = self.get_parameter(i+2, parameter_modes[1])
                if first != 0:
                    i = second
                else:
                    i += 3
            elif mode == 'JumpIfFalse':
                first = self.get_parameter(i + 1, parameter_modes[0])
                second = self.get_parameter(i + 2, parameter_modes[1])
                if first == 0:
                    i = second
                else:
                    i += 3
            elif mode == 'LessThan':
                first = self.get_parameter(i + 1, parameter_modes[0])
                second = self.get_parameter(i + 2, parameter_modes[1])
                pos = self.get_parameter(i + 3, 'Immediate')
                self.intcode[pos] = 1 if first < second else 0
                i += 4
            elif mode == 'Equals':
                first = self.get_parameter(i + 1, parameter_modes[0])
                second = self.get_parameter(i + 2, parameter_modes[1])
                pos = self.get_parameter(i + 3, 'Immediate')
                self.intcode[pos] = 1 if first == second else 0
                i += 4

            elif mode == 'Halt':
                break
            else:
                print('error')
                return 0
        return self.intcode

    def get_next_input(self):
        if self.inputs_used >= len(self.inputs):
            input_value = input('Enter an integer input : ')
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
        output = computer.process_code()
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
    # input_iterations = itertools.permutations(input_codes)
    outputs = []
    computers = []
    # for iteration in input_iterations:
    computers = []
    output = 0
    for i, input_code in enumerate(input_codes):
        computers.append(IntcodeComputer([i for i in intcode], [input_code, output], return_outputs=True))
        output = computers[i].process_code()
    for i in range(150):
        computers[i%5].inputs += [input_codes[i%5], output]
        output = computers[i%5].process_code()
    print(output)



if __name__ == "__main__":
    test_result = test()
    if test_result:
        print('Test passed')
    else:
        print('Test Failed')
        sys.exit()
    run_part_1()
    run_part_2()
