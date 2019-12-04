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
