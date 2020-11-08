import logging
from collections import defaultdict
from enum import Enum


class IntcodeHaltedException(Exception):
    pass


class IntcodeNeedInputException(Exception):
    pass


class IntcodeMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Intcode(object):
    """The Intcode computer used in 2019 adventofcode challenges."""

    def __init__(
        self,
        opcodes,
        noun=None,
        verb=None,
        input_data=None,
        pause_on_output=False,
        computer_name="intcode",
    ):
        if isinstance(opcodes, str):
            opcodes = [int(op) for op in opcodes.split(",")]

        self.opcodes = opcodes
        self.memory = defaultdict(int)
        for i, op in enumerate(opcodes):
            self.memory[i] = op

        self.noun = noun
        self.verb = verb

        if self.noun:
            self.memory[1] = self.noun
        if self.verb:
            self.memory[2] = self.verb

        self.input_data = input_data or list()
        self.pause_on_output = pause_on_output

        self.paused = self.halted = False

        self.pointer = 0
        self.relative_base = 0

        self.output_data = list()

        self.computer_name = computer_name

    def debug_log(self, msg):
        logging.debug(f"{self.computer_name}: {msg}")

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
        modes = [IntcodeMode(0)] * 3
        modes[0 : len(opcode[:-2])] = [
            IntcodeMode(int(i)) for i in reversed(opcode[:-2])
        ]
        return op, modes

    def execute(self):
        memory = self.memory
        loops = 0

        if self.halted:
            raise IntcodeHaltedException("The intcode computer has been halted!")

        if self.paused:
            self.debug_log(f"-- RESUME (at {self.pointer}) --")
            self.paused = False

        self.debug_log("Executing with parameters:")
        self.debug_log(f"  input_data: {self.input_data}")

        def get_offset(mode):
            if mode == IntcodeMode.RELATIVE:
                return self.relative_base
            return 0

        while True:
            if loops > 10:
                break

            i = self.pointer

            op, modes = self.parse_op(memory[i])
            self.debug_log(
                f"Processing op {op} at position {i} with modes {modes}"
                f" relative base {self.relative_base}..."
            )
            self.debug_log(f"  memory: {memory.values()}")

            #  ADD
            if op == 1:
                if modes[0] == IntcodeMode.IMMEDIATE:
                    s = memory[i + 1]
                else:
                    s = memory[memory[i + 1] + get_offset(modes[0])]

                if modes[1] == IntcodeMode.IMMEDIATE:
                    s += memory[i + 2]
                else:
                    s += memory[memory[i + 2] + get_offset(modes[1])]

                if modes[2] == IntcodeMode.IMMEDIATE:
                    memory[i + 3] = s
                else:
                    memory[memory[i + 3] + get_offset(modes[2])] = s

                self.pointer += 4
            #  MULTIPLY
            elif op == 2:
                if modes[0] == IntcodeMode.IMMEDIATE:
                    m = memory[i + 1]
                else:
                    m = memory[memory[i + 1] + get_offset(modes[0])]

                if modes[1] == IntcodeMode.IMMEDIATE:
                    m *= memory[i + 2]
                else:
                    m *= memory[memory[i + 2] + get_offset(modes[1])]

                if modes[2] == IntcodeMode.IMMEDIATE:
                    memory[i + 3] = m
                else:
                    memory[memory[i + 3] + get_offset(modes[2])] = m

                self.pointer += 4
            #  INPUT
            elif op == 3:
                try:
                    input_value = self.input_data.pop(0)
                except IndexError:
                    raise IntcodeNeedInputException("Input expected.")

                self.debug_log(f"Processing input value {input_value}...")
                if modes[0] == IntcodeMode.IMMEDIATE:
                    memory[i + 1] = input_value
                else:
                    memory[memory[i + 1] + get_offset(modes[0])] = input_value
                self.pointer += 2
            #  OUTPUT
            elif op == 4:
                if modes[0] == IntcodeMode.IMMEDIATE:
                    o = memory[i + 1]
                else:
                    o = memory[memory[i + 1] + get_offset(modes[0])]

                self.output_data.append(o)
                self.debug_log(f"Output data appended: {o}")
                self.pointer += 2

                if self.pause_on_output:
                    self.debug_log(f"-- PAUSE (will resume at {self.pointer}) --")
                    return list(memory.values())
            #  JUMP-IF-TRUE
            elif op == 5:
                if modes[0] == IntcodeMode.IMMEDIATE:
                    p = memory[i + 1]
                else:
                    p = memory[memory[i + 1] + get_offset(modes[0])]

                if p:
                    if modes[1] == IntcodeMode.IMMEDIATE:
                        self.pointer = memory[i + 2]
                    else:
                        self.pointer = memory[memory[i + 2] + get_offset(modes[1])]
                    if self.pointer == i:
                        logging.warning(f"Loop in op {op}, position {i}")
                        loops += 1
                else:
                    self.pointer += 3

            #  JUMP-IF-FALSE
            elif op == 6:
                if modes[0] == IntcodeMode.IMMEDIATE:
                    p = memory[i + 1]
                else:
                    p = memory[memory[i + 1] + get_offset(modes[0])]

                if p == 0:
                    if modes[1] == IntcodeMode.IMMEDIATE:
                        self.pointer = memory[i + 2]
                    else:
                        self.pointer = memory[memory[i + 2] + get_offset(modes[1])]
                    if self.pointer == i:
                        logging.warning(f"Loop in op {op}, position {i}")
                        loops += 1
                else:
                    self.pointer += 3
            #  LESS THAN
            elif op == 7:
                if modes[0] == IntcodeMode.IMMEDIATE:
                    p1 = memory[i + 1]
                else:
                    p1 = memory[memory[i + 1] + get_offset(modes[0])]

                if modes[1] == IntcodeMode.IMMEDIATE:
                    p2 = memory[i + 2]
                else:
                    p2 = memory[memory[i + 2] + get_offset(modes[1])]

                v = 1 if p1 < p2 else 0

                if modes[2] == IntcodeMode.IMMEDIATE:
                    memory[i + 3] = v
                else:
                    memory[memory[i + 3] + get_offset(modes[2])] = v
                self.pointer += 4
            #  EQUALS
            elif op == 8:
                if modes[0] == IntcodeMode.IMMEDIATE:
                    p1 = memory[i + 1]
                else:
                    p1 = memory[memory[i + 1] + get_offset(modes[0])]

                if modes[1] == IntcodeMode.IMMEDIATE:
                    p2 = memory[i + 2]
                else:
                    p2 = memory[memory[i + 2] + get_offset(modes[1])]

                v = 1 if p1 == p2 else 0

                if modes[2] == IntcodeMode.IMMEDIATE:
                    memory[i + 3] = v
                else:
                    memory[memory[i + 3] + get_offset(modes[2])] = v
                self.pointer += 4
            elif op == 9:
                if modes[0] == IntcodeMode.IMMEDIATE:
                    self.relative_base += memory[i + 1]
                else:
                    self.relative_base += memory[memory[i + 1] + get_offset(modes[0])]
                self.pointer += 2
            #  HALT
            elif op == 99:
                self.halted = True
                return list(memory.values())

            else:
                raise Exception(f"Unknown opcode [{op}]!")

        raise Exception("Unterminated program!")
