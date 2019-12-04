from aocd.models import Puzzle


def run_program(opcodes):
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


if __name__ == '__main__':
    puzzle = Puzzle(year=2019, day=2)
    opcodes = list(map(int, puzzle.input_data.split(',')))

    #  Per the written instructions
    opcodes[1] = 12
    opcodes[2] = 2

    output_codes = run_program(opcodes)

    puzzle.answer_a = output_codes[0]
