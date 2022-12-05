import pytest

from adventofcode.year2022.day5.solution import StackManager


@pytest.fixture(name="example_stack_definition")
def fixture_example_stack_definition():
    return """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".splitlines()


def test_example_stack(example_stack_definition):
    stack_manager = StackManager(example_stack_definition)

    assert len(stack_manager.stack_moves) == 4
    assert len(stack_manager.stacks) == 3
    assert stack_manager.stacks[0] == ["Z", "N"]
    assert stack_manager.stacks[1] == ["M", "C", "D"]
    assert stack_manager.stacks[2] == ["P"]

    stack_manager.move()
    assert len(stack_manager.stack_moves) == 3
    assert stack_manager.stacks[0] == ["Z", "N", "D"]
    assert stack_manager.stacks[1] == ["M", "C"]
    assert stack_manager.stacks[2] == ["P"]
    assert stack_manager.message == "DCP"

    stack_manager.move_all()
    assert stack_manager.message == "CMZ"
