import itertools
import math
import re
from dataclasses import dataclass
from typing import List

from aoc_components.input_getter import get_my_input

puzzle_input = get_my_input(2019, 12)


@dataclass()
class Vector:
    x: int
    y: int
    z: int

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(x=self.x + other.x,
                          y=self.y + other.y,
                          z=self.z + other.z,
                          )
        return NotImplemented

    @property
    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


@dataclass()
class Moon:
    id: int
    pos: Vector
    vel: Vector

    @property
    def pot(self):
        return self.pos.energy

    @property
    def kin(self):
        return self.vel.energy

    @property
    def total_energy(self):
        return self.pot * self.kin


@dataclass()
class MoonPart:
    id: int
    a: str
    p: int
    v: int

    @property
    def static(self):
        return self.id, self.p, self.v


moons: List[Moon] = []
moon_parts: List[MoonPart] = []
groups = []


def _import():
    for i, r in enumerate(puzzle_input.split("\n")):
        m = re.match(r"<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>", r.lower())
        x, y, z = map(int, (m[1], m[2], m[3]))
        moons.append(Moon(i, Vector(x, y, z), Vector(0, 0, 0)))
        moon_parts.extend([
            MoonPart(i, "x", x, 0),
            MoonPart(i, "y", y, 0),
            MoonPart(i, "z", z, 0),
        ])

    for A in ("x", "y", "z"):
        groups.append([p for p in moon_parts if p.a == A])


_import()


def apply_gravity_parts(parts: List[MoonPart]):
    done = []
    for a, b in itertools.product(parts, parts):
        pair = sorted((a.id, b.id))
        if a.id == b.id or pair in done:
            continue
        done.append(pair)
        if a.p != b.p:
            if a.p > b.p:
                a.v -= 1
                b.v += 1
            else:
                a.v += 1
                b.v -= 1


def apply_velocity_parts(parts: List[MoonPart]):
    for part in parts:
        part.p += part.v


def find_repeat(parts: List[MoonPart]):
    i_ = 0
    init = [p.static for p in parts]
    while True:
        apply_gravity_parts(parts)
        apply_velocity_parts(parts)
        current = [p.static for p in parts]
        i_ += 1
        if current == init:
            return i_


def part_2():
    def _d(a, b):
        return a * b // math.gcd(a, b)
    x_, y_, z_ = (find_repeat(p) for p in groups)
    return _d(_d(x_, y_), z_)


def apply_gravity():
    done = []
    for a, b in itertools.product(moons, moons):  # type: Moon, Moon
        pair = sorted((a.id, b.id))
        if a.id == b.id or pair in done:
            continue
        done.append(pair)
        if a.pos.x != b.pos.x:
            if a.pos.x > b.pos.x:
                a.vel.x -= 1
                b.vel.x += 1
            else:
                a.vel.x += 1
                b.vel.x -= 1

        if a.pos.y != b.pos.y:
            if a.pos.y > b.pos.y:
                a.vel.y -= 1
                b.vel.y += 1
            else:
                a.vel.y += 1
                b.vel.y -= 1

        if a.pos.z != b.pos.z:
            if a.pos.z > b.pos.z:
                a.vel.z -= 1
                b.vel.z += 1
            else:
                a.vel.z += 1
                b.vel.z -= 1


def apply_velocity():
    for moon in moons:
        moon.pos += moon.vel


def step(n=1):
    for _ in range(n):
        apply_gravity()
        apply_velocity()


def part_1(steps):
    step(steps)
    return sum((_.total_energy for _ in moons))


if __name__ == '__main__':
    p_1 = part_1(1000)
    p_2 = part_2()
    assert p_1 == 6220
    assert p_2 == 548525804273976
    print(f"Part 1: {p_1}. Part 2: {p_2}")
