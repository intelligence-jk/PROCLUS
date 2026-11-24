import random
from fractions import Fraction as F

import pytest

from worksheetgen import KINDS, make_question, make_worksheet, render
from worksheetgen.__main__ import main


def test_same_seed_same_sheet_and_different_seed_differs():
    a = make_worksheet(list(KINDS), 8, 5)
    b = make_worksheet(list(KINDS), 8, 5)
    c = make_worksheet(list(KINDS), 8, 6)
    assert a == b
    assert [q.text for q in a] != [q.text for q in c]


def test_linear_answers_satisfy_the_equation():
    rng = random.Random(0)
    for _ in range(300):
        q = make_question("linear", rng)
        a, b, c = q.data
        assert a * q.answer + b == c and q.answer.denominator == 1


def test_fraction_sum_answer_is_independently_correct():
    rng = random.Random(1)
    for _ in range(300):
        q = make_question("fraction-sum", rng)
        a, b, c, d = q.data
        assert q.answer == F(a * d + b * c, b * d)
        assert b != d and 0 < a < b and 0 < c < d


def test_percent_answers_independent_check():
    rng = random.Random(2)
    for _ in range(300):
        q = make_question("percent", rng)
        p, n = q.data
        assert q.answer * 100 == p * n
        q = make_question("percent-change", rng)
        v, p, up = q.data
        assert q.answer == (v + v * p / 100 if up else v - v * p / 100)


def test_no_repeated_questions_and_kinds_rotate():
    qs = make_worksheet(["linear", "percent"], 10, 3)
    assert len({q.text for q in qs}) == 10
    assert [q.kind for q in qs[:4]] == ["linear", "percent", "linear", "percent"]


def test_render_sheet_and_key():
    qs = make_worksheet(["fraction-sum"], 3, 1)
    sheet, key = render(qs, 1), render(qs, 1, key=True)
    assert sheet.startswith("# Worksheet (seed 1)") and key.startswith("# Answer key (seed 1)")
    assert "/" in key.splitlines()[2] or key.splitlines()[2][3:].isdigit()
    assert all(str(q.answer.numerator) not in sheet.splitlines()[0] for q in qs)


def test_errors():
    with pytest.raises(ValueError):
        make_question("nope", random.Random(0))
    with pytest.raises(ValueError):
        make_worksheet([], 3, 1)
    with pytest.raises(ValueError):
        make_worksheet(["percent-change"], 500, 1)  # fewer than 500 distinct questions exist


def test_cli(capsys):
    assert main(["--seed", "7", "-n", "4"]) == 0
    sheet = capsys.readouterr().out
    assert main(["--seed", "7", "-n", "4"]) == 0
    assert capsys.readouterr().out == sheet
    assert main(["--seed", "7", "-n", "4", "--key"]) == 0
    assert "Answer key" in capsys.readouterr().out
