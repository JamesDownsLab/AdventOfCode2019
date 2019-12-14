from intcode import IntcodeComputer, read_intcode_input_file

if __name__ == "__main__":
    # intcode = [104,1125899906842624,99]
    # intcode = [1102,34915192,34915192,7,4,7,99,0]
    # intcode = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    intcode = read_intcode_input_file('input.txt')
    computer = IntcodeComputer(intcode, [], return_outputs=False)
    outs = []
    while True:
        out = computer.run()
        if out is not None:
            # print(out)
            outs.append(out)
        else:
            break
    print(outs)
    # code = computer.intcode
    # print(code)