from aocd.models import Puzzle


def run_program(opcodes, noun=None, verb=None):

    if noun:
        opcodes[1] = noun
    if verb:
        opcodes[2] = verb

    for i in range(0, len(opcodes), 4):
        op = opcodes[i]

        if op == 1:
            opcodes[opcodes[i + 3]] = (opcodes[opcodes[i + 1]] +
                                       opcodes[opcodes[i + 2]])
        elif op == 2:
            opcodes[opcodes[i + 3]] = (opcodes[opcodes[i + 1]] *
                                       opcodes[opcodes[i + 2]])
        elif op == 99:
            return opcodes

        else:
            raise Exception(f'Unknown opcode [{op}]!')

    raise Exception('Unterminated program!')


def find_inputs(opcodes, output_0):
    for noun in range(100):
        for verb in range(100):
            output = run_program(opcodes.copy(), noun, verb)
            if output[0] == output_0:
                return (noun, verb)


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=2)
    opcodes = [int(op) for op in puzzle.input_data.split(',')]

    output_codes = run_program(opcodes.copy(), noun=12, verb=2)

    puzzle.answer_a = output_codes[0]
    b_tuple = find_inputs(opcodes, 19690720)
    puzzle.answer_b = 100 * b_tuple[0] + b_tuple[1]
