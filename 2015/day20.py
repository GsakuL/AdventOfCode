from aoc_components.puzzle_input import PuzzleInput
from itertools import product, permutations
from typing import List, Dict, Tuple, NamedTuple
from collections import defaultdict, UserDict
import re
from random import shuffle
import math


def divisors(n):
    divs = [1]
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            divs.extend([i, n//i])
    divs.extend([n])
    return set(divs)


if __name__ == "__main__":
    inp = int(PuzzleInput(__file__).get())

    house = inp
    for _ in reversed(range(inp)):
        div = divisors(_+1)
        p = sum(
            (10 * d for d in div)
        )
        if p >= inp:
            house = min(house, p)
    print(house)
