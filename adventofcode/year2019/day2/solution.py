from adventofcode.common.year2019.intcode_computer import Intcode


def find_inputs(opcodes, output_0):
    for noun in range(100):
        for verb in range(100):
            intcode = Intcode(opcodes, noun, verb)
            intcode.execute()
            if intcode.opcodes[0] == output_0:
                return (noun, verb)
