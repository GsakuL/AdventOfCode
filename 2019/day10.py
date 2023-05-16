import json
import math
from dataclasses import dataclass
from math import gcd
from typing import List

import numpy


class Point:
    def __init__(self, x, y, name=None):
        self.x = int(x)
        self.y = int(y)
        self.rho, self.phi = self.cart2pol(self.x, self.y)
        self._shorten = None
        self.name = name

    @staticmethod
    def rotate_phi(phi):
        phi -= math.pi/2
        if phi < 0:
            phi += 2 * math.pi
        return phi

    @property
    def t(self):
        return self.x, self.y

    # noinspection PyChainedComparisons
    @staticmethod
    def my_phi(x, y):
        """corrected phi for laser rotation"""
        if x == 0 and y >= 0:
            return 0
        if x > 0 and y > 0:
            return numpy.arctan(x / y)
        if x > 0 and y == 0:
            return math.pi / 2
        if x > 0 and y < 0:
            return numpy.arctan(x / abs(y)) + math.pi / 2
        if x == 0 and y < 0:
            return math.pi
        if x < 0 and y < 0:
            return numpy.arctan(abs(x) / abs(y)) + math.pi
        if x < 0 and y == 0:
            return 3 * math.pi / 2
        if x < 0 and y > 0:
            return numpy.arctan(abs(x) / y) + (3 * math.pi / 2)
        raise ValueError

    @classmethod
    def cart2pol(cls, x, y):
        rho = numpy.sqrt(x ** 2 + y ** 2)
        # phi = numpy.arctan2(y, x)
        phi = cls.my_phi(x, y)
        return rho, phi

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented

    def shorten(self):
        if not self._shorten:
            d = gcd(self.x, self.y)
            n = Point(self.x / d, self.y / d)
            self._shorten = n
        return self._shorten

    def __str__(self):
        n = self.name or ""
        if n:
            n = f" '{n}'"
        return f"Point({self.x}, {self.y})<{self.rho}, {self.phi}rad>{n}"

    __repr__ = __str__

    def short_str(self):
        return str((self.x, self.y))


@dataclass()
class Asteroid:
    pos: Point
    can_see = 0

    def __eq__(self, other):
        if isinstance(other, Asteroid):
            return self.pos == other.pos
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.pos.__hash__()

    def __str__(self):
        return f"Asteroid({self.pos.short_str()}, {self.can_see})"

    __repr__ = __str__


with open("day10_data.json", "r") as fp:
    puzzle_data: dict = json.load(fp)


def parse_map(map_: List[str]):
    asteroids = []
    for y, line in enumerate(map_):
        for x, c in enumerate(line):
            if c != ".":
                asteroids.append(Asteroid(Point(x, y, name=c)))
    return asteroids


def get_seen_asteroids(map_, x, y):
    this = Point(x, y)
    distances = set()
    for y_, row in enumerate(map_):
        for x_, ast in enumerate(row):
            if (not isinstance(ast, int)) or x == x_ and y == y_:
                continue
            distances.add((this - Point(x_, y_)).shorten())
    return len(distances)


def get_seen_asteroids2(map_, x, y):
    this = Point(x, y)
    distances = set()
    for y_, row in enumerate(map_):
        for x_, ast in enumerate(row):
            if (not isinstance(ast, int)) or x == x_ and y == y_:
                continue
            new = (this - Point(x_, y_))
            further = [d for d in distances if (d.phi == new.phi or d.shorten() == new.shorten()) and d.rho > new.rho]
            if further:
                for f in further:
                    distances.remove(f)
            distances.add(new)
    s2 = sorted(distances, key=lambda p: -p.phi)
    return len(distances)


def get_relative(origin: Point, child: Point):
    return Point(child.x - origin.x, origin.y - child.y, name=child.name)


def get_absolute(origin: Point, relative: Point):
    return Point(origin.x + relative.x, origin.y - relative.y, name=relative.name)


def get_closest_asteroids(asteroids: List[Asteroid], a: Asteroid):
    closest = set()
    for a_ in asteroids:
        if a == a_:
            continue
        new = get_relative(a.pos, a_.pos)
        same_path = [d for d in closest if (d.phi == new.phi or d.shorten() == new.shorten())]
        further_seen = [d for d in same_path if d.rho > new.rho]
        new_is_further = any((True for a in same_path if a.rho < new.rho))
        if further_seen:
            for f in further_seen:
                closest.remove(f)
        if not new_is_further:
            closest.add(new)
    return closest


def get_vaporization(asteroids: List[Asteroid], a: Asteroid):
    vaporized = {a.pos.t}
    while len(vaporized) != len(asteroids):
        closest_points = {}
        for b in asteroids:
            if b.pos.t not in vaporized:
                dx, dy = b.pos.x - a.pos.x, b.pos.y - a.pos.y
                dx, dy = dx // math.gcd(dx, dy), dy // math.gcd(dx, dy)
                c_x, c_y = closest_points.get((dx, dy), (float('inf'), float('inf')))
                if abs(b.pos.x - a.pos.x) + abs(b.pos.y - a.pos.y) < abs(c_x - a.pos.x) + abs(c_y - a.pos.y):
                    closest_points[(dx, dy)] = b.pos.t
        vaporized = vaporized.union(set(sorted(closest_points.values(), key=lambda p: -math.atan2(p[0] - a.pos.x, p[1] - a.pos.y))))
    return vaporized


def walk_map(asteroids):
    for a in asteroids:
        seen = len(get_closest_asteroids(asteroids, a))
        a.can_see = seen
    return asteroids


def get_best(map_):
    asteroids = parse_map(map_)
    res = walk_map(asteroids)
    m = max(asteroids, key=lambda a: a.can_see)
    return m


def run_part_1():
    b = get_best(puzzle_data.get("my_puzzle_input"))
    assert 347 == b.can_see
    assert (26, 36) == b.pos.t


def run_part_2():
    inp = puzzle_data["my_puzzle_input"]
    asteroids = parse_map(inp)
    p = Point(26, 36)
    a = next((_ for _ in asteroids if _.pos == p))
    v = get_vaporization(asteroids, a)
    print(v)



def run_examples():
    for ex in puzzle_data["examples_1"]:  # type: dict
        b = get_best(ex["data"])
        print(f"expected: {ex['pos']},{ex['amount']}. Got: {b}")


def run_example_2():
    ex = puzzle_data["examples_2"][0]
    d = ex["data"]
    asteroids = parse_map(d)
    p = Point(*ex["pos"])
    a = next((_ for _ in asteroids if _.pos == p))
    s = get_closest_asteroids(asteroids, a)
    print(s)


def run_example_2_big():
    ex = puzzle_data["examples_1"][0]
    d = ex["data"]
    asteroids = parse_map(d)
    p = Point(*ex["pos"])
    a = next((_ for _ in asteroids if _.pos == p))
    leftover = 200
    while True:
        dest = sorted(get_closest_asteroids(asteroids, a), key=lambda _: (_.phi, _.rho), reverse=False)
        absolutes = [get_absolute(a.pos, b) for b in dest]
        if len(dest) < leftover:
            leftover -= len(dest)
            for a_ in dest:
                asteroids.remove(a_)
        else:
            t = absolutes[leftover-1]
            print(t)
            return t


def run_test():
    a = [
        Point(0, 5),
        Point(5, 5),
        Point(5, 0),
        Point(5, -5),
        Point(0, -5),
        Point(-5, -5),
        Point(-5, 0),
        Point(-5, 5),
    ]

    b = sorted(a, key=lambda p: p.phi, reverse=False)
    breakpoint()


if __name__ == '__main__':
    # run_examples()
    run_part_2()
    # run_example_2()
    # run_example_2_big()
    # run_test()
