def run_program(opcodes, noun=None, verb=None):

    if noun:
        opcodes[1] = noun
    if verb:
        opcodes[2] = verb

    move_forward = 0

    for i, op in enumerate(opcodes):

        if move_forward > 0:
            move_forward = move_forward - 1
            continue

        op = opcodes[i]

        #  ADD
        if op == 1:
            opcodes[opcodes[i + 3]] = (opcodes[opcodes[i + 1]] +
                                       opcodes[opcodes[i + 2]])
            move_forward = 3
        #  MULTIPLY
        elif op == 2:
            opcodes[opcodes[i + 3]] = (opcodes[opcodes[i + 1]] *
                                       opcodes[opcodes[i + 2]])
            move_forward = 3
        #  HALT
        elif op == 99:
            return opcodes

        else:
            raise Exception(f'Unknown opcode [{op}]!')

    raise Exception('Unterminated program!')
