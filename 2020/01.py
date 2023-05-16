from aoc_components import PuzzleInput
from typing import List

def one(numbers: List[int]):
    for ix, x in enumerate(numbers):
        for iy, y in enumerate(numbers):
            if ix == iy:
                continue
            if x+y == 2020:
                return (x, y)

def two(numbers: List[int]):
    for ix, x in enumerate(numbers):
        for iy, y in enumerate(numbers):
            for iz, z in enumerate(numbers):
                if ix == iy or ix == iz or iy == iz:
                    continue
                if x+y+z == 2020:
                    return (x, y, z)

if __name__ == "__main__":
    numbers = PuzzleInput(__file__).as_list("\n", int)
    x, y = one(numbers)
    print(f"{x=} {y=} | {x*y}")

    x, y, z = two(numbers)
    print(f"{x=} {y=} {z=} | {x*y*z}")
