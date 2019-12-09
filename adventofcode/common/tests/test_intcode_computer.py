import pytest

from adventofcode.common.year2019.intcode_computer import Intcode


@pytest.mark.parametrize("opcodes,output_codes", [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
])
def test_intcode_execute_result(opcodes, output_codes):
    assert Intcode(opcodes).execute() == output_codes


@pytest.mark.parametrize("opcodes", [
    [3, 0, 0, 0, 99],
    [1, 1, 1, 4, 99, 5, 6, 0, 0],
])
def test_intcode_execute_bad_op(opcodes):
    with pytest.raises(Exception) as e:
        Intcode(opcodes).execute()
        assert 'Unknown opcode' in str(e.value)


@pytest.mark.parametrize("opcodes", [
    [],
    [3, 0, 0, 0],
    [1, 1, 1, 4, 99, 5, 6, 0],
])
def test_intcode_execute_early_exit(opcodes):
    with pytest.raises(Exception) as e:
        Intcode(opcodes).execute()
        assert 'Unterminated program' in str(e.value)


LONG_EXAMPLE = ('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,'
                '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,'
                '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99')


@pytest.mark.parametrize("opcodes,input_data,last_output", [
    ('3,9,8,9,10,9,4,9,99,-1,8', [8], 1),
    ('3,9,8,9,10,9,4,9,99,-1,8', [7], 0),
    ('3,9,8,9,10,9,4,9,99,-1,8', [9], 0),
    ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', [0], 0),
    ('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', [8], 1),
    ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', [0], 0),
    ('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', [8], 1),
    (LONG_EXAMPLE, [7], 999),
    (LONG_EXAMPLE, [8], 1000),
    (LONG_EXAMPLE, [9], 1001),
])
def test_opcodes_five_through_eight(opcodes, input_data, last_output):
    intcode = Intcode(opcodes, input_data=input_data)
    intcode.execute()
    assert intcode.last_output == last_output


@pytest.mark.parametrize("opcodes,input_data,output", [
    ('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99', [], [
        int(i) for i in
        '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'.split(',')
    ]),
    ('104,1125899906842624,99', [], [1125899906842624]),
])
def test_relative_mode_and_big_numbers(opcodes, input_data, output):
    intcode = Intcode(opcodes, input_data=input_data)
    intcode.execute()
    assert intcode.output_data == output


def test_big_number_indefinite_test_case():
    """For whatever reason, the output here is just 'a 16-digit number'."""
    intcode = Intcode('1102,34915192,34915192,7,4,7,99,0')
    intcode.execute()
    assert len(str(intcode.last_output)) == 16


def test_pre_execution_output():
    intcode = Intcode([])
    assert intcode.last_output is None
