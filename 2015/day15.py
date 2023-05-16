from aoc_components.input_getter import get_my_input
from typing import List
from dataclasses import dataclass, field
import itertools
import operator
import functools
from collections import Counter
import re
inp = get_my_input(__file__)


@dataclass(unsafe_hash=True)
class Ingredient:
    name: str = field(hash=True)
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int
    compund: bool = False

    def sum_up(self, factor: int):
        cp = self.capacity * factor
        dr = self.durability * factor
        fl = self.flavor * factor
        tx = self.texture * factor
        cl = self.calories * factor

        return Ingredient(self.name, cp, dr, fl, tx, cl, compund=True)


r = re.compile(r"^([a-zA-Z]+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)$")


def parse(line: str) -> Ingredient:
    global r
    m = r.match(line)
    if not m:
        raise RuntimeError()
    return Ingredient(m[1], int(m[2]), int(m[3]), int(m[4]), int(m[5]), int(m[6]))


def clamp_zero(i: int):
    if i < 0:
        return 0
    return i


def main():
    ingredients: List[Ingredient] = []

    for line in inp.splitlines():
        ingredients.append(parse(line))

    max_part1 = 0
    max_part2 = 0
    for comb in itertools.combinations_with_replacement(ingredients, 100):
        c = Counter(comb)
        s = {}
        k: Ingredient
        v: int
        totals: List[Ingredient] = [k.sum_up(v) for k, v in c.items()]

        for p in ("capacity", "durability", "flavor", "texture"):
            s[p] = clamp_zero(sum(
                (getattr(i, p) for i in totals)
             ))
        t: Ingredient
        cal = sum(
            (t.calories for t in totals)
        )
        red = functools.reduce(operator.mul, s.values(), 1)
        if cal == 500:
            max_part2 = max(max_part2, red)
        max_part1 = max(max_part1, red)
    print(max_part1)
    print(max_part2)


if __name__ == "__main__":
    main()
