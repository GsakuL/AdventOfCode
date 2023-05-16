from pathlib import Path
import shutil
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, ArgumentTypeError
from typing import Any
from datetime import datetime


neg_inf: int = float("-inf")  # type: ignore


def int_aoc(value: Any, ma: int, mi: int = neg_inf):
    ivalue = int(value)
    if (ivalue < mi) or (ivalue > ma):
        raise ArgumentTypeError(f"{ivalue} is an invalid. Minimum {mi}; max {ma}")
    return ivalue


def year_aoc(value: Any):
    return int_aoc(value, 2015)


def day_aoc(value: Any):
    return int_aoc(value, 25, 1)


def get_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--year", type=year_aoc, default=datetime.today().year)
    parser.add_argument("--start", type=day_aoc, default=1)
    parser.add_argument("--end", "--stop", type=day_aoc, default=25)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if (args.end < args.start):
        raise ValueError("start must be lower than or equal end")
    return args


if __name__ == "__main__":
    args = get_args()
    template: Path = Path(__file__).parent / "aoc_components" / "utils" / "day_template.py"
    target: Path = Path(__file__).parent / str(args.year)
    target.mkdir(exist_ok=True)

    initpy = target / "__init__.py"
    initpy.touch(exist_ok=True)

    for i in range(args.start, args.end + 1):
        file = target / f"{i:02d}.py"
        if file.exists() and (not args.overwrite):
            continue
        shutil.copy(template, file)
