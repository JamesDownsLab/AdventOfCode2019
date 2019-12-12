with open('input.txt', 'r') as f:
    file = f.read()
intcode = file.split(',')
intcode = [int(i) for i in intcode]
print(len(intcode))

opcode_instructions = {1: 'Add', 2: 'Multiply', 3: 'Input', 4:'Output', 99: 'Halt'}
parameter_modes = {0: 'Position', 1: 'Immediate'}

def process_code(intcode):
    i = 0
    while i < len(intcode):
        opcode = intcode[i]
        mode, parameter_modes = process_opcode(opcode)
        if mode == 'Add':
            first = intcode[intcode[i+1]] if parameter_modes[0] == 'Position' else intcode[i+1]
            second = intcode[intcode[i+2]] if parameter_modes[1] == 'Position' else intcode[i+2]
            pos = intcode[i+3]
            intcode[pos] = first + second
            i += 4
        elif mode == 'Multiply':
            first = intcode[intcode[i + 1]] if parameter_modes[0] == 'Position' else intcode[i + 1]
            second = intcode[intcode[i + 2]] if parameter_modes[1] == 'Position' else intcode[i + 2]
            pos = intcode[i+3]
            intcode[pos] = first * second
            i += 4
        elif mode == 'Input':
            pos = intcode[i+1]
            input_value = int(input('Enter an integer input: '))
            intcode[pos] = input_value
            i += 2
        elif mode == 'Output':
            output = intcode[intcode[i+1]] if parameter_modes[0] == 'Position' else intcode[i + 1]
            print(output)
            i += 2
        elif mode == 'Halt':
            break
        else:
            print('error')
            return 0
    return intcode

def process_opcode(opcode):
    opcode = str(opcode)
    mode = opcode[-2:]
    p_modes = []
    for p in range(3, 6):
        if p <= len(opcode):
            p_modes.append(1 if opcode[-p] == '1' else 0)
        else:
            p_modes.append(0)
    return opcode_instructions[int(mode)], [parameter_modes[p] for p in p_modes]

code = process_code(intcode)
print(code)
