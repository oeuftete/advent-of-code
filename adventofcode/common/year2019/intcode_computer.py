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

        self.pointer = 0

        self.input_data = input_data or list()
        self.output_data = list()

    @property
    def last_output(self):
        if self.output_data:
            return self.output_data[-1]
        return

    @classmethod
    def parse_op(cls, opcode):
        """Parse an opcode, and return the op and a list of modes."""
        opcode = str(opcode)
        op = int(opcode[-2:])
        modes = [0, 0, 0]
        modes[0:len(opcode[:-2])] = [int(i) for i in reversed(opcode[:-2])]
        return op, modes

    def execute(self):
        opcodes = self.opcodes
        loops = 0

        logging.debug('Executing with parameters:')
        logging.debug(f'  input_data: {self.input_data}')

        while True:
            if loops > 10:
                break

            i = self.pointer

            op, modes = self.parse_op(opcodes[i])
            logging.debug(f'Processing op {op} at position {i}...')
            logging.debug(f'  Opcodes: {opcodes}')

            #  ADD
            if op == 1:
                s = opcodes[i + 1] if modes[0] else opcodes[opcodes[i + 1]]
                s += opcodes[i + 2] if modes[1] else opcodes[opcodes[i + 2]]
                if modes[2]:
                    opcodes[i + 3] = s
                else:
                    opcodes[opcodes[i + 3]] = s
                self.pointer += 4
            #  MULTIPLY
            elif op == 2:
                m = opcodes[i + 1] if modes[0] else opcodes[opcodes[i + 1]]
                m *= opcodes[i + 2] if modes[1] else opcodes[opcodes[i + 2]]
                if modes[2]:
                    opcodes[i + 3] = m
                else:
                    opcodes[opcodes[i + 3]] = m
                self.pointer += 4
            #  INPUT
            elif op == 3:
                input_value = self.input_data.pop(0)
                logging.debug(f'Processing input value {input_value}...')
                if modes[0]:
                    opcodes[i + 1] = input_value
                else:
                    opcodes[opcodes[i + 1]] = input_value
                self.pointer += 2
            #  OUTPUT
            elif op == 4:
                if modes[0]:
                    o = opcodes[i + 1]
                else:
                    o = opcodes[opcodes[i + 1]]

                self.output_data.append(o)
                logging.debug(f'Output data appended: {o}')
                self.pointer += 2
            #  JUMP-IF-TRUE
            elif op == 5:
                p = opcodes[i + 1] if modes[0] else opcodes[opcodes[i + 1]]

                if p:
                    self.pointer = (opcodes[i + 2]
                                    if modes[1] else opcodes[opcodes[i + 2]])
                    if self.pointer == i:
                        logging.warning(f'Loop in op {op}, position {i}')
                        loops += 1
                else:
                    self.pointer += 3

            #  JUMP-IF-FALSE
            elif op == 6:
                p = opcodes[i + 1] if modes[0] else opcodes[opcodes[i + 1]]

                if p == 0:
                    self.pointer = (opcodes[i + 2]
                                    if modes[1] else opcodes[opcodes[i + 2]])
                    if self.pointer == i:
                        logging.warning(f'Loop in op {op}, position {i}')
                        loops += 1
                else:
                    self.pointer += 3
            #  LESS THAN
            elif op == 7:
                p1 = (opcodes[i + 1] if modes[0] else opcodes[opcodes[i + 1]])
                p2 = (opcodes[i + 2] if modes[1] else opcodes[opcodes[i + 2]])
                if p1 < p2:
                    if modes[2]:
                        opcodes[i + 3] = 1
                    else:
                        opcodes[opcodes[i + 3]] = 1
                else:
                    if modes[2]:
                        opcodes[i + 3] = 0
                    else:
                        opcodes[opcodes[i + 3]] = 0
                self.pointer += 4
            #  EQUALS
            elif op == 8:
                p1 = (opcodes[i + 1] if modes[0] else opcodes[opcodes[i + 1]])
                p2 = (opcodes[i + 2] if modes[1] else opcodes[opcodes[i + 2]])
                if p1 == p2:
                    if modes[2]:
                        opcodes[i + 3] = 1
                    else:
                        opcodes[opcodes[i + 3]] = 1
                else:
                    if modes[2]:
                        opcodes[i + 3] = 0
                    else:
                        opcodes[opcodes[i + 3]] = 0
                self.pointer += 4
            #  HALT
            elif op == 99:
                return opcodes

            else:
                raise Exception(f'Unknown opcode [{op}]!')

        raise Exception('Unterminated program!')
