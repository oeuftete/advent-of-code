import logging


class Intcode(object):
    """The Intcode computer used in 2019 adventofcode challenges."""
    def __init__(self, opcodes, noun=None, verb=None, input_data=None):
        if isinstance(opcodes, str):
            opcodes = [int(op) for op in opcodes.split(',')]

        self.opcodes = opcodes

        self.noun = noun
        self.verb = verb

        if self.noun:
            self.opcodes[1] = self.noun
        if self.verb:
            self.opcodes[2] = self.verb

        self.input_data = input_data or list()
        self.output_data = list()

    @classmethod
    def parse_op(cls, opcode):
        """Parses an opcode, and return the op and a list of modes."""
        opcode = str(opcode)
        op = int(opcode[-2:])
        modes = [0, 0, 0]
        modes[0:len(opcode[:-2])] = [int(i) for i in reversed(opcode[:-2])]
        return op, modes

    def execute(self):
        move_forward = 0
        opcodes = self.opcodes

        for i, op in enumerate(opcodes):

            if move_forward > 0:
                move_forward = move_forward - 1
                continue

            op, modes = self.parse_op(opcodes[i])

            #  ADD
            if op == 1:
                s = opcodes[i + 1] if modes[0] else opcodes[opcodes[i + 1]]
                s += opcodes[i + 2] if modes[1] else opcodes[opcodes[i + 2]]
                if modes[2]:
                    opcodes[i + 3] = s
                else:
                    opcodes[opcodes[i + 3]] = s
                move_forward = 3
            #  MULTIPLY
            elif op == 2:
                m = opcodes[i + 1] if modes[0] else opcodes[opcodes[i + 1]]
                m *= opcodes[i + 2] if modes[1] else opcodes[opcodes[i + 2]]
                if modes[2]:
                    opcodes[i + 3] = m
                else:
                    opcodes[opcodes[i + 3]] = m
                move_forward = 3
            #  INPUT
            elif op == 3:
                if modes[0]:
                    opcodes[i + 1] = self.input_data.pop(0)
                else:
                    opcodes[opcodes[i + 1]] = self.input_data.pop(0)
                move_forward = 1
            #  OUTPUT
            elif op == 4:
                if modes[0]:
                    o = opcodes[i + 1]
                else:
                    o = opcodes[opcodes[i + 1]]

                self.output_data.append(o)
                logging.debug(f'Output data: {o}')
                move_forward = 1
            #  HALT
            elif op == 99:
                return opcodes

            else:
                raise Exception(f'Unknown opcode [{op}]!')

        raise Exception('Unterminated program!')


def run_program(opcodes, noun=None, verb=None, input_data=None):
    """A thin wrapper to run an Intcode program."""
    intcode = Intcode(opcodes, noun, verb, input_data)
    return intcode.execute()
