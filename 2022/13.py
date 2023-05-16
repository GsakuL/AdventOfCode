from __future__ import annotations

import functools
import itertools
import re
from typing import Any, Dict, Generator, List, NamedTuple, Optional, Set, TypeAlias, TypedDict, Union

from aoc_components import PuzzleInput

DataPacket: TypeAlias = Union[int, list['DataPacket']]

Pair = tuple[DataPacket, DataPacket]


def verify(value: Any, invert=False):
    test = not not value
    if invert:
        test = not test
    if test:
        return value
    raise ValueError(value)


def parse(puzzle: str) -> Generator[Pair, None, None]:
    lines = puzzle.splitlines()
    while lines:
        yield (eval(verify(lines.pop(0))), eval(verify(lines.pop(0))))
        try:
            lines.pop(0)
        except IndexError:
            pass


def normalize(left: int | list, right: int | list) -> tuple[int, int] | tuple[list, list]:
    if isinstance(left, int) and isinstance(right, list):
        return ([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return (left, [right])
    return (left, right)


def get(items: list, index: int):
    if 0 <= index < len(items):
        return items[index]
    return None


def compare(left: DataPacket, right: DataPacket):
    left, right = normalize(left, right)
    if left is None and right is not None:
        return True
    if left is not None and right is None:
        return False
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        if left > right:
            return False
    if isinstance(left, list) and isinstance(right, list):
        max_ = max(len(left), len(right))
        for i in range(max_):
            a = get(left, i)
            b = get(right, i)
            sub_result = compare(a, b)
            if sub_result is not None:
                return sub_result


def part_1(pairs: list[Pair]):
    for left, right in pairs:
        compare(left, right)


TEST_PUZZLE = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

DIV_2 = [[2]]
DIV_6 = [[6]]


def ungroup(items: list[Pair]):
    for a, b in items:
        yield a
        yield b


def flatten(items: list):
    for i in items:
        if isinstance(i, list):
            yield from flatten(i)
        else:
            yield i


def part_2(pairs: list[Pair]):
    ungrouped = list(ungroup(pairs))
    absolute_list = [list(flatten(u)) for u in ungrouped]
    lens = [len(a) for a in absolute_list]
    max_len = max(lens)
    print(f"{max_len=}")

    # max_len = max((sum((1 for _ in flatten(u))) for u in ungrouped))

    def key(x: list):
        new = list(flatten(x))
        new.extend([float('-inf')] * (max_len - len(x)))
        return new

    total_order: list = sorted(ungrouped, key=key)
    # for item in total_order:
    #    print(item)
    indexe = (total_order.index(DIV_2) + 1) * (total_order.index(DIV_6) + 1)
    print(f"Part 2= {indexe}")
    # 14_773 too low


def part_2_smart(pairs: list[Pair]):
    ungrouped = list(ungroup(pairs))
    div_two = 1  # 1-indexed
    div_six = 2  # 1-indexed and adjusted for div_two
    for packet in ungrouped:
        div_two += compare(packet, DIV_2)
        div_six += compare(packet, DIV_6)
    print(f"Part 2= {div_two*div_six}")


def main():
    puzzle = PuzzleInput(__file__).get()
    # puzzle = TEST_PUZZLE
    pairs = list(parse(puzzle))
    # print(compare(*pairs[3]))
    in_order = sum(compare(a, b) * (i + 1) for i, (a, b) in enumerate(pairs))
    print(f"Part 1={in_order}")

    part_2_smart(pairs)


if __name__ == "__main__":
    main()
