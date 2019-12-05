from adventofcode.common.year2019.intcode_computer import run_program


def find_inputs(opcodes, output_0):
    for noun in range(100):
        for verb in range(100):
            output = run_program(opcodes.copy(), noun, verb)
            if output[0] == output_0:
                return (noun, verb)
