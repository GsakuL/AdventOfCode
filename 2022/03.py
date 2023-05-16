import re
from typing import Dict, Generator, List, NamedTuple, Optional, Sequence, Set, TypedDict
import string
from aoc_components import PuzzleInput

priority = {t[0]: t[1]+1 for t in zip(string.ascii_lowercase + string.ascii_uppercase, range(100))}

def group(items: list[str], size: int = 3) -> Generator[list[str], None, None]:
    group = []
    for i in items:
        group.append(i)
        if len(group) >= size:
            yield group
            group = []
    if group:
        yield group

def verify_single(items: set[str]):
    if len(items) != 1:
            raise ValueError(items)
    return items.pop()

if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).get()
    
    values = 0 
    for line in puzzle.splitlines():
        h = len(line)//2
        a = set(line[:h])
        b = set(line[h:])
        intersection = a.intersection(b)
        duplicate = verify_single(intersection)
        values += priority[duplicate]

    print(f"Part 1: {values}")

    values_2 = 0
    for grouping in group(puzzle.splitlines()):
        a,b,c = (set(x) for x in grouping)
        inter = a.intersection(b).intersection(c)
        same = verify_single(inter)
        values_2 += priority[same]
    
    print(f"Part 2: {values_2}")