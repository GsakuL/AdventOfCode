import copy
import re
from typing import Dict, Iterable, List, NamedTuple, Optional, Set, TypedDict

from aoc_components import PuzzleInput


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point'):
        return self.__class__(self.x + other.x, self.y + other.y)


Scan = dict[Point, str]

DOWN = Point(0, 1)
DOWN_LEFT = Point(-1, 1)
DOWN_RIGHT = Point(1, 1)


def srange(start: int, end: int) -> Iterable[int]:
    if start > end:
        return range(start, end - 1, -1)
    return range(start, end + 1)


SAND_SPAWN = Point(500, 0)


def find_lowest(scan: Scan):
    max(p.y for p in scan)


def draw_lines(scan: Scan, points: list[Point]):
    for start, end in zip(points, points[1:]):
        for x in srange(start.x, end.x):
            for y in srange(start.y, end.y):
                scan[Point(x, y)] = '#'


def parse(puzzle: str):
    scan = Scan()
    for line in puzzle.splitlines():
        points: list[Point] = [Point(*(int(n) for n in p.split(","))) for p in line.split(" -> ")]
        draw_lines(scan, points)
    return scan


def get_next_pos(scan: Scan, current: Point, lowest: int):
    for possible in (DOWN, DOWN_LEFT, DOWN_RIGHT):
        new = current + possible
        if new not in scan:
            return new


def get_last_pos(scan: Scan, current: Point, lowest: int, part2: bool):
    while True:
        new = get_next_pos(scan, current, lowest)
        if not new:
            return current
        if part2:
            if new.y == (lowest + 2):
                return current
            if new == SAND_SPAWN:
                return None
        else:
            if new.y > lowest:
                return None
        current = new


def simulate(scan: Scan, lowest: int, part2: bool):
    units = 0
    while True:
        # draw(scan, lowest, part2)
        sand = SAND_SPAWN
        new = get_last_pos(scan, sand, lowest, part2)
        if not new or new in scan:
            return units  # cannot rest
        units += 1
        scan[new] = 'o'


def draw(scan: Scan, lowest: int, part2: bool):
    max_x = max(p.x for p in scan)
    min_x = min(p.x for p in scan)
    block = "█"
    horiz_frame = block * ((max_x - min_x) + 3)
    buffer = horiz_frame + "\n"

    for y in range(lowest + 1 + part2):
        buffer += block
        for x in range(min_x, max_x + 1):
            current = Point(x, y)
            txt = scan.get(current)
            if current == SAND_SPAWN:
                txt = "*" if txt else "+"
            buffer += txt or " "
        buffer += block + "\n"
    buffer += horiz_frame + "\n"
    print(buffer)


TEST_DATA = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def main():
    # puzzle = TEST_DATA
    puzzle = PuzzleInput(__file__).get()
    scan = parse(puzzle)
    scan2 = copy.copy(scan)

    lowest = max(p.y for p in scan)
    units = simulate(scan, lowest, False)
    print(f"Part 1= {units}")

    # just wait a few secs...
    units2 = simulate(scan2, lowest, True)
    print(f"Part 2= {units2}")


if __name__ == "__main__":
    main()
