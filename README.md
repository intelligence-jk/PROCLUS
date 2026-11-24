# worksheet-gen

Generate seeded practice worksheets with an exact answer key.

## What it solves
A tutor or a student wants fresh practice questions on a skill, with answers that are certain to be right, and wants to be able to regenerate the same sheet later. Give it a seed, a number of questions and the kinds you want, and it prints the worksheet; the same seed with `--key` prints the answer key. Four kinds are included: linear equations, adding fractions, percentage of an amount and percentage change. Pure Python 3.10+, standard library only. All the questions are generated from number patterns, none are taken from any book or paper.

## Example
```bash
python -m worksheetgen --seed 7 -n 4
python -m worksheetgen --seed 7 -n 4 --key
```
```
# Worksheet (seed 7)

1. Solve 4x - 3 = -23
2. Work out 1/2 + 2/4 as a fraction in its simplest form
3. Find 60% of 40
4. 400 is increased by 20%. What is the new value?
```
```
# Answer key (seed 7)

1. -5
2. 1
3. 24
4. 480
```
Choose kinds with `--kinds linear percent`. The kinds rotate through the sheet, and no question repeats.

## The maths behind it
Answers are built first, then the question is made from them, and every answer is an exact `Fraction`. A linear question picks `a` and the answer `x`, then sets `c = a x + b`, so `a x + b = c` has the whole-number solution `x` by construction (here 4 x (-5) - 3 = -23). A fraction sum is `a/b + c/d = (ad + bc)/(bd)`, reduced by `Fraction`. A percentage is `p x n / 100`, and a change is `v (100 +- p) / 100`. The tests re-derive each answer independently, for example by substituting `x` back into the equation, over hundreds of random questions.

## Install and run
```bash
python -m pip install -e .
python -m worksheetgen --seed 7 -n 6
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
