"""python -m worksheetgen --seed 7 -n 6 [--kinds linear percent] [--key]"""
import argparse
import sys

from .core import KINDS, make_worksheet, render


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python -m worksheetgen")
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("-n", type=int, default=8)
    p.add_argument("--kinds", nargs="+", default=list(KINDS), choices=list(KINDS))
    p.add_argument("--key", action="store_true", help="print the answer key instead of the questions")
    a = p.parse_args(argv)
    try:
        qs = make_worksheet(a.kinds, a.n, a.seed)
    except ValueError as e:
        print(f"Cannot make a worksheet: {e}", file=sys.stderr)
        return 1
    sys.stdout.write(render(qs, a.seed, a.key))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
