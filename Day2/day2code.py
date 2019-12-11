# 1202 Program Alarm

with open('input.txt', 'r') as f:
    file = f.read()
intcode = file.split(',')
intcode = [int(i) for i in intcode]



def process_code(intcode):
    for i in range(0, len(intcode), 4):
        opcode = intcode[i]
        if opcode == 99:
            break
        first, second, pos = intcode[intcode[i+1]], intcode[intcode[i+2]], intcode[i+3]
        if opcode == 1:
            intcode[pos] = first + second
        elif opcode == 2:
            intcode[pos] = first * second
        else:
            print('error')
            return 0
    return intcode

intcode[1] = 12
intcode[2] = 2
print(process_code(intcode.copy())[0])


with open('input.txt', 'r') as f:
    file = f.read()
intcode = file.split(',')
intcode = [int(i) for i in intcode]


want = 19690720
x = range(100)
y = range(100)
for noun in x:
    for verb in y:
        intcode[1] = noun
        intcode[2] = verb
        out = process_code(intcode.copy())[0]
        if out == want:
            print(out, noun, verb)
            correct_noun = noun
            correct_verb = verb


answer = (100 * correct_noun) + correct_verb
print(answer)