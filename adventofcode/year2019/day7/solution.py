from itertools import permutations
import logging
import math

from adventofcode.common.year2019.intcode_computer import Intcode


class AmplificationMaximizer(object):
    def __init__(self, opcodes, amplifier_count=5, initial_input_signal=0):
        self.opcodes = opcodes
        self.amplifier_count = amplifier_count
        self.initial_input_signal = initial_input_signal

        self.max_phase_sequence = None

    @property
    def max_output_signal(self):
        max_phase_sequence = None
        max_output_signal = -math.inf

        for phase_sequence in permutations(range(self.amplifier_count)):
            input_signal = self.initial_input_signal
            logging.debug(f'Testing sequence {phase_sequence}...')
            for i in range(self.amplifier_count):
                amplifier = Intcode(
                    self.opcodes, input_data=[phase_sequence[i], input_signal])
                amplifier.execute()
                input_signal = amplifier.last_output

            if amplifier.last_output > max_output_signal:
                max_output_signal = amplifier.last_output
                max_phase_sequence = phase_sequence
                logging.debug(f'Found better output [{max_output_signal}]'
                              f' with {phase_sequence}')

        self.max_phase_sequence = max_phase_sequence
        return max_output_signal
