import operator
import re
from itertools import chain
from typing import Dict, List, NamedTuple, Optional, Set, TypedDict

from aoc_components import PuzzleInput, remove_all


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Point'):
        return self.__class__(self.x + other.x, self.y + other.y)


DELTAS = (Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1))


class Sensor(NamedTuple):
    pos: Point
    beacon: Point


class Row(NamedTuple):
    middle: int
    width: int
    y_level: int


def parse(puzzle: str):

    def point(txt: str):
        a, b = txt.split(",")
        return Point(int(a), int(b))

    # Sensor at x=3391837, y=2528277: closest beacon is at x=3448416, y=2478759
    for line in puzzle.splitlines():
        line = remove_all(line, "Sensor at", "closest beacon is at", " ", "x=", "y=").strip()
        sens, beac = line.split(":")
        yield Sensor(point(sens), point(beac))


def calculate_sensor_row(sensor: Sensor) -> Row:
    p = sensor.pos
    b = sensor.beacon
    width = abs(p.x - b.x)
    return Row(p.x, width, p.y)


Y = 2_000_000


def mark_range(blocked: set[Point], sensor: Sensor):
    row = calculate_sensor_row(sensor)
    if sensor.pos.y <= Y <= row.y_level or sensor.pos.y >= Y >= row.y_level:
        diff = abs(Y - row.y_level)
    elif sensor.pos.y <= row.y_level <= Y or sensor.pos.y >= row.y_level >= Y:
        diff = -abs(Y - row.y_level)
    else:
        diff = abs(sensor.pos.y - row.y_level) - abs(sensor.pos.y - Y)
    return row._replace(y_level=Y, width=row.width + diff)


def draw(blocked: set[Point], sensors: list[Sensor]):
    mapping = {s.pos: "S" for s in sensors}
    mapping.update({s.beacon: "B" for s in sensors})

    min_x = min(p.x for p in chain(blocked, mapping.keys()))
    max_x = max(p.x for p in chain(blocked, mapping.keys()))

    min_y = min(p.y for p in chain(blocked, mapping.keys()))
    max_y = max(p.y for p in chain(blocked, mapping.keys()))

    buffer = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            p = Point(x, y)
            txt = mapping.get(p)
            if not txt and p in blocked:
                txt = "#"
            buffer += (txt or ".")
        buffer += "\n"
    print(buffer.strip())
    print()


def part_1(sensors: list[Sensor]):
    total_blocked = set[Point]()
    for sensor, beacon in sensors:
        if sensor != Point(8, 7):
            continue
        blocked = set[Point]()
        found = False
        current = {sensor}
        while not found and current:
            c = current.pop()
            blocked.add(c)
            for d in DELTAS:
                new = d + c
                if new == beacon:
                    found = True
                if new not in blocked:
                    current.add(new)
                blocked.add(new)
            draw(blocked, sensors)
        total_blocked = total_blocked.union(blocked)
    return total_blocked


TEST_DATA = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


def main():
    puzzle = TEST_DATA
    # puzzle = PuzzleInput(__file__).get()
    sensors = list(parse(puzzle))
    draw({}, sensors)
    #part_1(sensors)


if __name__ == "__main__":
    main()
