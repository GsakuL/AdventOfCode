import re
from typing import Dict, List, NamedTuple, Optional, Set, TypedDict

from aoc_components import PuzzleInput

example_data_1 = """
16
10
15
5
1
11
7
19
6
12
4
"""

example_data_2 = """
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""


def parse(data: str):
    vals = sorted((int(n) for n in data.splitlines() if n))

    return vals + [vals[-1] + 3]


def calc(data: List[int]):
    diffs = [0] * 4
    current = 0
    for num in data:
        dif = num - current
        if dif > 3:
            raise ValueError(dif)
        diffs[dif] = diffs[dif] + 1
        current = num
    return diffs


def calc_2(data: List[int], total: int, last=0, index=0):
    if index >= total:
        return 0
    value = data[index]

    if (value - last) > 3:
        return 0

    if (index + 1) == total:
        return 1

    pass
    return sum(calc_2(data, total, value, index + i) for i in (1, 2))
    for n in data:
        pass


if __name__ == "__main__":
    ex1 = parse(example_data_1)
    print(calc(ex1))

    ex2 = parse(example_data_2)
    print(calc(ex2))

    puzzle = PuzzleInput(__file__)()
    p = parse(puzzle)
    r = calc(p)
    print(f"result1={r[1] * r[3]}")

    r2 = calc_2(p, len(p))  # exponential!

    print()
