from collections import defaultdict
import logging
import re

from aocd import get_data

logging.basicConfig(level=logging.INFO)


class SampleParseException(Exception):
    pass


OP_CODES = {
    'ADDR': lambda cpu, a, b, c: cpu.set_r(c,
                                           cpu.r(a) + cpu.r(b)),
    'ADDI': lambda cpu, a, b, c: cpu.set_r(c,
                                           cpu.r(a) + b),
    'MULR': lambda cpu, a, b, c: cpu.set_r(c,
                                           cpu.r(a) * cpu.r(b)),
    'MULI': lambda cpu, a, b, c: cpu.set_r(c,
                                           cpu.r(a) * b),
    'BANR': lambda cpu, a, b, c: cpu.set_r(c,
                                           cpu.r(a) & cpu.r(b)),
    'BANI': lambda cpu, a, b, c: cpu.set_r(c,
                                           cpu.r(a) & b),
    'BORR': lambda cpu, a, b, c: cpu.set_r(c,
                                           cpu.r(a) | cpu.r(b)),
    'BORI': lambda cpu, a, b, c: cpu.set_r(c,
                                           cpu.r(a) | b),
    'SETR': lambda cpu, a, b, c: cpu.set_r(c, cpu.r(a)),
    'SETI': lambda cpu, a, b, c: cpu.set_r(c, a),
    'GTIR': lambda cpu, a, b, c: cpu.set_r(c, 1 if a > cpu.r(b) else 0),
    'GTRI': lambda cpu, a, b, c: cpu.set_r(c, 1 if cpu.r(a) > b else 0),
    'GTRR': lambda cpu, a, b, c: cpu.set_r(c, 1 if cpu.r(a) > cpu.r(b) else 0),
    'EQIR': lambda cpu, a, b, c: cpu.set_r(c, 1 if a == cpu.r(b) else 0),
    'EQRI': lambda cpu, a, b, c: cpu.set_r(c, 1 if cpu.r(a) == b else 0),
    'EQRR': lambda cpu, a, b, c: cpu.set_r(c, 1
                                           if cpu.r(a) == cpu.r(b) else 0),
}


class Cpu():
    def __init__(self, registers=None):
        self.registers = registers if registers else [0, 0, 0, 0]

    def r(self, n):
        return self.registers[n]

    def set_r(self, n, v):
        self.registers[n] = v

    def op(self, opcode, a, b, c):
        OP_CODES[opcode](self, a, b, c)


class CpuNumberedOps(Cpu):
    def __init__(self, registers=None):
        super(CpuNumberedOps, self).__init__(registers)

        #  Hand-created by looking at monitor.possible_opcode_matches,
        #  then just manually assigning each number to an op.  This could be
        #  automated by looking for each set of 1 and each op in only one set,
        #  assigning, eliminating those from remaining sets, repeating until
        #  complete.
        self.op_map = [
            'ADDI', 'EQRR', 'BORR', 'GTRI', 'ADDR', 'SETI', 'MULI', 'BANI',
            'BANR', 'GTRR', 'SETR', 'GTIR', 'BORI', 'EQRI', 'EQIR', 'MULR'
        ]

    def op_by_number(self, n, a, b, c):
        self.op(self.op_map[n], a, b, c)


class CpuMonitorSample():
    def __init__(self, before, operation, after):
        self.before = before
        self.operation = operation
        self.after = after

    @property
    def possible_opcodes(self):
        hits = list()
        for opcode in OP_CODES.keys():
            logging.debug('Before sample: {}'.format(self.before))
            c = Cpu(list(self.before))

            logging.debug('Before: {}'.format(c.registers))
            logging.debug('Applying: {}'.format(opcode))

            c.op(opcode, *(self.operation[1:]))

            logging.debug('After: {}'.format(c.registers))

            if c.registers == self.after:
                logging.debug('Hit: {}'.format(opcode))
                hits.append(opcode)

        return hits

    @property
    def opcode_number(self):
        return self.operation[0]


class CpuMonitor():
    def __init__(self, lines):
        self.lines = lines
        self.samples = list()
        self.data = list()
        self._parse()
        self.possibilities = defaultdict(lambda: set(OP_CODES.keys()))

    def find_ambiguous(self, ambiguity_threshold):
        count = 0
        for sample in self.samples:
            if len(sample.possible_opcodes) >= ambiguity_threshold:
                count += 1

        return count

    @property
    def possible_opcode_matches(self):
        for sample in self.samples:
            self.possibilities[sample.opcode_number] = (
                self.possibilities[sample.opcode_number] &  # noqa: W504
                set(sample.possible_opcodes))
        return self.possibilities

    def _parse(self):
        BEFORE_LINE = re.compile(r'Before:\s*\[(\d), (\d), (\d), (\d)\]')
        AFTER_LINE = re.compile(r'After:\s*\[(\d), (\d), (\d), (\d)\]')

        is_in_sample = False
        before = operation = after = None
        blank_lines = 0

        for line in self.lines:
            if line == "":
                blank_lines += 1
                continue

            if blank_lines > 1:
                self.data.append(list(map(int, line.split())))
                continue

            blank_lines = 0
            if not is_in_sample:
                m = re.match(BEFORE_LINE, line)
                if m:
                    is_in_sample = True
                    before = list(map(int, list(m.groups())))
            else:  # in sample
                if not operation:
                    operation = list(map(int, line.split()))
                else:
                    m = re.match(AFTER_LINE, line)
                    if m:
                        after = list(map(int, list(m.groups())))
                        self.samples.append(
                            CpuMonitorSample(before, operation, after))
                        before = operation = after = None
                        is_in_sample = False
                    else:
                        logging.error('Samples so far: {}'.format(
                            len(self.samples)))
                        raise SampleParseException('line = %s' % line)


if __name__ == '__main__':
    data = get_data(year=2018, day=16)
    lines = data.split('\n')
    monitor = CpuMonitor(lines)

    print("Problem 1:", monitor.find_ambiguous(3))

    cpu = CpuNumberedOps()
    for d in monitor.data:
        cpu.op_by_number(*d)
    print("Problem 2:", cpu.registers[0])
