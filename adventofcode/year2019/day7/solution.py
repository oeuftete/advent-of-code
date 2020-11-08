from itertools import permutations
import logging
import math

from adventofcode.common.year2019.intcode_computer import Intcode


class AmplificationMaximizer(object):
    def __init__(
        self, opcodes, amplifier_count=5, initial_input_signal=0, feedback=False
    ):
        self.opcodes = opcodes
        self.amplifier_count = amplifier_count
        self.initial_input_signal = initial_input_signal
        self.feedback = feedback

        self.amplifiers = self.reset_amplifiers()
        self.max_phase_sequence = None

    def reset_amplifiers(self):

        self.amplifiers = [
            Intcode(
                self.opcodes, computer_name="amp-{i}", pause_on_output=self.feedback
            )
            for i in range(self.amplifier_count)
        ]

    @property
    def max_output_signal(self):
        max_phase_sequence = None
        max_output_signal = -math.inf
        n_amps = self.amplifier_count

        phase_sequence_range = (
            range(n_amps, n_amps * 2) if self.feedback else range(n_amps)
        )

        for phase_sequence in permutations(phase_sequence_range):
            input_signal = self.initial_input_signal
            logging.debug(f"Testing sequence {phase_sequence}...")

            self.reset_amplifiers()

            first_execution_loop = True

            while True:
                for i, amplifier in enumerate(self.amplifiers):
                    if first_execution_loop:
                        input_data = [phase_sequence[i], input_signal]
                    else:
                        input_data = [input_signal]

                    amplifier.input_data = input_data
                    amplifier.execute()
                    input_signal = amplifier.last_output

                if amplifier.halted:
                    break

                first_execution_loop = False  # for feedback loops only

            if amplifier.last_output > max_output_signal:
                max_output_signal = amplifier.last_output
                max_phase_sequence = phase_sequence
                logging.debug(
                    f"Found better output [{max_output_signal}]"
                    f" with {phase_sequence}"
                )

        self.max_phase_sequence = max_phase_sequence
        return max_output_signal
