"""Seeded practice worksheets with an exact answer key. Same seed, same sheet."""
from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Question:
    kind: str
    text: str
    answer: F
    data: tuple  # the numbers used, so anyone can re-check the answer


def _linear(r: random.Random) -> Question:
    a = r.choice([2, 3, 4, 5, 6, 7])
    x = r.randint(-9, 12)
    b = r.randint(-15, 15)
    c = a * x + b
    sign = "+" if b >= 0 else "-"
    return Question("linear", f"Solve {a}x {sign} {abs(b)} = {c}", F(x), (a, b, c))


def _fraction_sum(r: random.Random) -> Question:
    denominators = [2, 3, 4, 5, 6, 8, 9, 10, 12]
    b = r.choice(denominators)
    d = r.choice([x for x in denominators if x != b])
    a, c = r.randint(1, b - 1), r.randint(1, d - 1)
    return Question("fraction-sum", f"Work out {a}/{b} + {c}/{d} as a fraction in its simplest form", F(a, b) + F(c, d), (a, b, c, d))


def _percent(r: random.Random) -> Question:
    p = r.choice([5, 10, 12, 15, 20, 25, 30, 40, 45, 60, 75])
    n = r.choice([40, 60, 80, 120, 150, 200, 240, 360, 400, 500])
    return Question("percent", f"Find {p}% of {n}", F(p * n, 100), (p, n))


def _percent_change(r: random.Random) -> Question:
    v = r.choice([80, 120, 200, 250, 400, 600])
    p = r.choice([10, 20, 25, 30, 50])
    up = r.random() < 0.5
    word = "increased" if up else "decreased"
    return Question("percent-change", f"{v} is {word} by {p}%. What is the new value?", F(v) * (100 + (p if up else -p)) / 100, (v, p, up))


KINDS = {"linear": _linear, "fraction-sum": _fraction_sum, "percent": _percent, "percent-change": _percent_change}


def make_question(kind: str, rng: random.Random) -> Question:
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}; choose from {', '.join(KINDS)}")
    return KINDS[kind](rng)


def make_worksheet(kinds: list[str], n: int, seed: int) -> list[Question]:
    if n < 1 or not kinds:
        raise ValueError("need at least one question and one kind")
    rng = random.Random(seed)
    out, seen = [], set()
    attempts = 0
    while len(out) < n:
        attempts += 1
        if attempts > 50 * n:
            raise ValueError("could not make that many different questions")
        q = make_question(kinds[len(out) % len(kinds)], rng)
        if q.text not in seen:
            seen.add(q.text)
            out.append(q)
    return out


def _fmt(a: F) -> str:
    return str(a.numerator) if a.denominator == 1 else f"{a.numerator}/{a.denominator}"


def render(questions: list[Question], seed: int, key: bool = False) -> str:
    title = "Answer key" if key else "Worksheet"
    lines = [f"# {title} (seed {seed})", ""]
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {_fmt(q.answer)}" if key else f"{i}. {q.text}")
    return "\n".join(lines) + "\n"
