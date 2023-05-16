from typing import Dict, List, NamedTuple, Tuple

import sympy
from scipy.optimize import minimize_scalar

from aoc_components.input_getter import get_my_input


class Ingredient(NamedTuple):
    amount: int
    element: str


RD = Dict[Ingredient, List[Ingredient]]

puzzle_input = get_my_input(2019, 14)

class Pool:
    def __init__(self, rd_: RD):
        self.pool: Dict[str, int] = dict()
        self.rd = rd_
        self.elements = set(self.get_all_elements())
        self.symbols = {s.name: s for s in sympy.symbols(" ".join(self.elements))}
        self.base_r = dict()
        self.equations = list(self.make_equations())

    def add_output(self, i: Ingredient, multi: int = 1):
        self.pool[i.element] = self.pool.get(i.element, 0) + (i.amount * multi)
        needed = find_recipe(i, self.rd)[1]
        for n in needed:
            self.pool[n.element] = self.pool.get(n.element, 0) - (n.amount * multi)

    def scale(self, multi: int):
        for k, v in self.pool.items():
            self.pool[k] = v * multi

    @property
    def needs(self):
        return (Ingredient(a, e) for e, a in self.pool.items() if a < 0 and e != "ORE")

    @property
    def is_satisfied(self):
        return not any(self.needs)

    @property
    def needed_ore(self):
        return abs(self.pool.get("ORE", 0))

    @property
    def produced_fuel(self):
        return abs(self.pool.get("FUEL", 0))

    @property
    def is_balanced(self):
        for k, v in self.pool.items():
            if k in ("FUEL", "ORE"):
                continue
            if v != 0:
                return False
        return True

    def get_all_elements(self):
        for k, v in self.rd.items():
            yield k.element
            for v_ in v:
                yield v_.element

    def make_equations(self):
        for k, v in self.rd.items():  # type: Ingredient, List[Ingredient]
            #if any((r for r in v if r.element == "ORE")):
            #    self.base_r[k] = v
            f = 0 + k.amount * self.symbols[k.element]
            for i in v:
                f = f - i.amount * self.symbols[i.element]
            yield (k.element, k.amount), f

    @staticmethod
    def needs_intermediary(e: sympy.Expr):
        for arg in e.args:
            a = arg.args
            if a and a[0] < 0 and a[1] not in ("FUEL", "ORE"):
                return True
        return False

    def consolidate_equation(self, e: sympy.Expr):
        other = {_[0]: _[1] for _ in self.equations if _[1] != e}
        while self.needs_intermediary(e):
            for arg in e.args:
                if isinstance(arg, sympy.Symbol):
                    n, s = 1, arg
                else:
                    n, s = arg.args
                r = [(k[1], v) for k, v in other.items() if k[0] == s.name]
                if r and n < 0:
                    r = r[0]
                    multi = ceil_div(int(n), r[0])
                    e += multi*r[1]
                    breakpoint()

        breakpoint()

    def simplify(self, rl: List[Ingredient], rd: RD):
        new = []
        old_keys = []
        for r in rl:
            u = [(k, v) for k, v in rd.items() if any((n for n in v if n.element == r.element))]
            key = [k for k in rd.keys() if k.element == r.element]
            if not u:
                continue
            if len(u) > 1 or any((_ for _ in u[0][1] if _.element == "ORE")) or not key:
                new.append(r)
            else:
                key = key[0]
                needed = rd[key]
                multi = ceil_div(r.amount, key.amount)
                new.extend([Ingredient(i.amount * multi, i.element) for i in needed])
                old_keys.append(key)
                pass
        for key in old_keys:
            rd.pop(key)
        return new, rd

    def consolidate(self, rl: List[Ingredient]):
        new = []
        for k in {k.element for k in rl}:
            new.append(Ingredient(sum([_.amount for _ in rl if _.element == k]), k))
        return new




def parse_ingredients(ing: str):
    result = []
    for i in ing.split(","):
        i = i.strip()
        a, e = i.split(" ")
        result.append(Ingredient(int(a), e))
    return result


def import_file():
    recipes: RD = dict()
    for r in puzzle_input.split("\n"):
        in_, out_ = r.split("=>")
        recipes[parse_ingredients(out_)[0]] = parse_ingredients(in_)
    return recipes


def find_recipe(r: Ingredient, rd_: RD) -> Tuple[Ingredient, List[Ingredient]]:
    for k, v in rd_.items():
        if k.element == r.element:
            return k, v


def ceil_div(a: int, b: int) -> int:
    d = abs(a) // abs(b)
    m = (1 if (abs(a) % abs(b)) else 0)
    return m + d


def calculate(pool_: Pool, rd_: RD, start_fuel=1):
    pool_.add_output(Ingredient(1, "FUEL"), start_fuel)
    while not pool_.is_satisfied:
        need = next(pool_.needs)
        next_r = find_recipe(need, rd_)[0]
        n = ceil_div(need.amount, next_r.amount)
        m = 1
        pool_.add_output(next_r, n)


def part_1(fuel=1):
    rd = import_file()
    pool = Pool(rd)
    calculate(pool, rd, start_fuel=fuel)
    return pool


def part_0():
    rd = import_file()
    pool = Pool(rd)
    calculate(pool, rd)
    fuel = Ingredient(1, 'FUEL')
    rd_ = rd.copy()

    fuel_e = [_ for _ in pool.equations if _[0][0] == "FUEL"][0]

    pool.consolidate_equation(fuel_e[1])

    a = 0
    while a != len(rd_):
        a = len(rd_)
        i, d = pool.simplify(rd_.get(fuel), rd_)
        i = pool.consolidate(i)
        rd_[fuel] = i
    return pool


def part_2():
    p_ = part_1()
    p_2 = part_1(2)
    fuel_1 = p_.needed_ore  # 783895
    target = 1000000000000
    ratio = int(target / fuel_1)

    def ore_left(fuel_):
        ore = part_1(fuel=int(fuel_)).needed_ore
        left = target - ore
        if left < 0:
            return abs(left) * 100
        return left

    fuel = minimize_scalar(
        ore_left,
        bracket=(ratio, 2*ratio)
    ).x

    return int(fuel)


if __name__ == '__main__':
    #print(f"Part 1: {part_1().needed_ore}")
    print(f"Part 2: {part_2()}")
