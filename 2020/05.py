from aoc_components import PuzzleInput

from typing import NamedTuple, TypedDict, Optional, List
import re

def ged_id_part(num: str, low: int, high: int, upper: str, lower: str, start: int, stop: int):
    for i in range(start, stop-1):
        j = num[i]
        if j == lower:
            high = ((high-low) // 2)+low
        elif j == upper:
            low = (high+low+1)//2
        else:
            raise ValueError((i, j))
    # if low != high:
    #    raise ValueError((low, high))
    j = num[stop-1]
    if j == lower:
        return low
    elif j == upper:
        return high
    raise ValueError((stop, j))

def get_id_row(num: str):
    return ged_id_part(num, 0, 127, "B", "F", 0, 7)
    low = 0
    high = 127
    for i in range(7):
        j = num[i]
        if j == "F":
            high = ((high-low) // 2)+low
        elif j == "B":
            low = (high+low+1)//2
        else:
            raise ValueError((i, j))

    print((low, high))


def get_id_col(num: str):
    return ged_id_part(num, 0, 7, "R", "L", 7, 10)


def get_id(num: str):
    return (get_id_row(num) * 8) + get_id_col(num)


def my_id(seats: List[int]):
    for x in range(seats[0], seats[-1]+1):
        if x not in seats:
            if x-1 in seats and x+1 in seats:
                return x

if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).as_list("\n")
    seats = sorted((get_id(s) for s in puzzle))
    print(f"{seats[-1]}")
    print(f"{my_id(seats)=}")
