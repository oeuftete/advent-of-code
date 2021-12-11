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

    assert len(p.incomplete_lines) == 5
    assert p.middle_score == 288957


@pytest.mark.parametrize(
    "line,is_corrupt,is_incomplete,first_illegal,autocompletion",
    [
        ("{([(<{}[<>[]}>{[]{[(<()>", True, False, "}", ""),
        ("[({(<(())[]>[[{[]{<()<>>", False, True, "", "}}]])})]"),
    ],
)
def test_parser_line(line, is_corrupt, is_incomplete, first_illegal, autocompletion):
    pl = ParserLine(line)

    assert pl.is_corrupt == is_corrupt
    assert pl.is_incomplete == is_incomplete
    assert pl.first_illegal == first_illegal
    assert pl.autocompletion == autocompletion
