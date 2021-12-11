import pytest

from adventofcode.year2021.day10.solution import Parser, ParserLine


@pytest.fixture(name="example_lines")
def fixture_example_lines():
    return """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip().splitlines()


def test_example_lines(example_lines):
    p = Parser(lines=example_lines)

    assert len(p.corrupt_lines) == 5
    assert p.syntax_score == 26397


@pytest.mark.parametrize(
    "line,is_corrupt,first_illegal",
    [
        ("{([(<{}[<>[]}>{[]{[(<()>", True, "}"),
        ("[({(<(())[]>[[{[]{<()<>>", False, ""),
    ],
)
def test_parser_line(line, is_corrupt, first_illegal):
    pl = ParserLine(line)

    assert pl.is_corrupt == is_corrupt
    assert pl.first_illegal == first_illegal
