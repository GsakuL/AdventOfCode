import re
from typing import Dict, List, NamedTuple, Optional, Set, TypedDict

from aoc_components import PuzzleInput

def range_subset(first, second, full_contain=True):
    # https://stackoverflow.com/questions/32480423/how-to-check-if-a-range-is-a-part-of-another-range-in-python-3-x
    if not first:
        return True  # empty range is subset of anything
    if not second:
        return False  # non-empty range can't be subset of empty range
    if len(first) > 1 and first.step % second.step:
        return False  # must have a single value or integer multiple step
    a = first.start in second 
    b = first[-1] in second
    return (a and b, a or b)

def parse(txt: str):
    for line in txt.splitlines():
        a, b = line.split(",")

        a_a, a_z = a.split("-")
        b_a, b_z = b.split("-")

        range_a = range(int(a_a), int(a_z)+1)
        range_b = range(int(b_a), int(b_z)+1)
        yield (range_a, range_b)

if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).get()
    pairs = list(parse(puzzle))
    
    count_1 = 0
    count_2 = 0
    for a, b in pairs:
        add_1, add_2 = range_subset(a, b)
        add_3, add_4 = range_subset(b, a)
        if add_1 or add_3:
            count_1 += 1
        if add_2 or add_4:
            count_2 += 1
    print(f"Part 1: {count_1}")
    print(f"Part 2: {count_2}")
