from aoc_components import PuzzleInput
from typing import List, Set, Callable
import string

test_1 = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""

T_call = Callable[[Set[str], Set[str]], Set[str]]


def count(yn: List[str], call: T_call) -> Set[str]:
    result = set(yn[0])
    for x in yn[1:]:
        # result = result.intersection(set(x))
        # result = result.union(set(x))
        result = call(result, set(x))
    return result


def parse(raw: str, call: T_call):
    current = []
    result: List[Set[str]] = []
    for line in raw.splitlines():
        if not line.strip():
            if current:
                result.append(count(current, call))
                current = []
        else:
            current.append(line)
    if current:
        result.append(count(current, call))
    return result


def calc_sum(counted: List[Set[str]]):
    return sum((len(c) for c in counted))


def intersect(a: Set[str], b: Set[str]):
    return a.intersection(b)


def union(a: Set[str], b: Set[str]):
    return a.union(b)


if __name__ == "__main__":
    puzzle = PuzzleInput(__file__)()
    # spuzzle = test_1
    counted_1 = parse(puzzle, union)
    sum_1 = calc_sum(counted_1)
    print(f"{sum_1=}")

    counted_2 = parse(puzzle, intersect)
    sum_2 = calc_sum(counted_2)
    print(f"{sum_2=}")
