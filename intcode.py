class IntcodeComputer:

    opcode_instructions = {1: 'Add', 2: 'Multiply', 3: 'Input', 4:'Output', 5: 'JumpIfTrue', 6: 'JumpIfFalse',
                       7: 'LessThan', 8: 'Equals', 9: 'ChangeBase', 99: 'Halt'}
    parameter_modes = {0: 'Position', 1: 'Immediate', 2: 'Relative'}

    def __init__(self, intcode, inputs, return_outputs=False):
        self.intcode = intcode
        self.size = len(self.intcode)
        self.intcode += [0 for i in range(10000000)]
        self.inputs = inputs
        self.inputs_used = 0
        self.return_outputs = return_outputs
        self.i = 0
        self.relative_base = 0

    def run(self):
        while self.i < len(self.intcode):
            opcode = self.intcode[self.i]
            mode, parameter_modes = self.process_opcode(opcode)
            self.section = self.intcode[self.i:self.i+5]
            if mode == 'Halt':
                break
            functions = {'Add': self.add,
                         'Multiply': self.multiply,
                         'Input': self.input,
                         'Output': self.output,
                         'JumpIfTrue': self.jumpiftrue,
                         'JumpIfFalse': self.jumpiffalse,
                         'LessThan': self.lessthan,
                         'Equals': self.equal,
                         'ChangeBase': self.changebase,
                         'Halt': self.halt}

            out = functions[mode](parameter_modes)
            if out is not None:
                return out

    def add(self, modes):
        first = self.get_parameter(self.i+1, modes[0])
        second = self.get_parameter(self.i+2, modes[1])
        pos = self.get_parameter(self.i+3, modes[2], write_mode=True)
        self.intcode[pos] = first + second
        self.i += 4

    def multiply(self, modes):
        first = self.get_parameter(self.i + 1, modes[0])
        second = self.get_parameter(self.i + 2, modes[1])
        pos = self.get_parameter(self.i + 3, modes[2], write_mode=True)
        self.intcode[pos] = first * second
        self.i += 4

    def input(self, modes):
        pos = self.get_parameter(self.i+1, modes[0], write_mode=True)
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
        pos = self.get_parameter(self.i+3, modes[2], write_mode=True)
        self.intcode[pos] = 1 if first < second else 0
        self.i += 4

    def equal(self, modes):
        first = self.get_parameter(self.i+1, modes[0])
        second = self.get_parameter(self.i+2, modes[1])
        pos = self.get_parameter(self.i+3, modes[2], write_mode=True)
        self.intcode[pos] = 1 if first == second else 0
        self.i += 4

    def changebase(self, modes):
        first = self.get_parameter(self.i+1, modes[0])
        self.relative_base += first
        self.i += 2

    def halt(self, modes):
        return 'HALT'

    def get_next_input(self):
        if self.inputs_used >= len(self.inputs):
            input_value = int(input('Enter an integer input : '))
        else:
            input_value = self.inputs[self.inputs_used]
        self.inputs_used += 1
        return input_value

    def get_parameter(self, pos, mode, write_mode=False):
        pos = self.intcode[pos]
        if mode == 'Position':
            if not write_mode:
                param = self.intcode[pos]
            else:
                param = pos
        elif mode == 'Immediate':
            if not write_mode:
                param = pos
            else:
                print('error')
        elif mode == 'Relative':
            if not write_mode:
                param = self.intcode[self.relative_base+pos]
            else:
                param = pos + self.relative_base
        return param

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

    def add_inputs(self, additional_input):
        self.inputs.append(additional_input)


def read_intcode_input_file(file):
    with open(file, 'r') as f:
        file = f.read()
    intcode = file.split(',')
    intcode = [int(i) for i in intcode]
    return intcode