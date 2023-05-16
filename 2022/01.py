import re
from typing import Dict, List, NamedTuple, Optional, Set, TypedDict

from aoc_components import PuzzleInput

if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).get()

    carry = []
    running = 0
    for line in puzzle.splitlines():
        line = line.strip()
        if not line:
            carry.append(running)
            running = 0
        else:
            running += int(line)
    carry = sorted(carry, reverse=True)
    print(f"Part 1: sum={carry[0]}")
    print(f"Part 2: top 3 sum={sum(carry[:3])}")
