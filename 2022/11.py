import math
import operator
import re
from functools import reduce
from typing import Callable, Dict, List, NamedTuple, Optional, Set, TypedDict

from aoc_components import PuzzleInput

test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

operations = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
}


class Group:

    def __init__(self) -> None:
        self.monkeys: dict[int, 'Monkey'] = {}
        self._super_modulo: int | None = None

    def __getitem__(self, i: int):
        return self.monkeys[i]

    def __setitem__(self, i: int, item: 'Monkey'):
        self.monkeys[i] = item

    def __contains__(self, item):
        return item in self.monkeys

    @property
    def super_modulo(self):
        if not self._super_modulo:
            raise ValueError("super_modulo not set")
        return self._super_modulo

    @super_modulo.setter
    def super_modulo(self, value: int):
        self._super_modulo = value


class Monkey:
    SuperModulo = -1

    def __init__(self, id_: int, group: Group, items: list[int], operation: Callable[[int], int], divide: bool,
                 divide_by: int, throw_true: int, throw_false: int) -> None:
        if id_ in group:
            raise ValueError(f"Monkey {id_} already present")

        self.id_ = id_
        self.group = group
        self.items = items
        self.operation = operation
        self.throw_true = throw_true
        self.throw_false = throw_false
        self.divide_by = divide_by
        self.divide = divide
        self.inspected = 0
        group[id_] = self

    @classmethod
    def parse(cls, group: Group, lines: list[str], divide: bool):

        def remove(txt: str, *vals):
            for v in vals:
                txt = txt.replace(v, "")
            return txt

        id_ = int(lines.pop(0)[7:-1])
        items = [int(i) for i in remove(lines.pop(0), "Starting items:", " ").split(",")]
        operation = cls.parse_operation(lines.pop(0))
        divide_by = int(remove(lines.pop(0), "Test: divisible by", " "))
        if_true = int(remove(lines.pop(0), "If true: throw to monkey", " "))
        if_false = int(remove(lines.pop(0), "If false: throw to monkey", " "))
        monkey = cls(id_, group, items, operation, divide, divide_by, if_true, if_false)
        return monkey

    @classmethod
    def parse_all(cls, text: str, divide=True):
        group = Group()
        for markup in text.split("\n\n"):
            cls.parse(group, markup.splitlines(), divide)
        divisions = [m.divide_by for m in group.monkeys.values()]
        mod = math.lcm(*divisions)
        group.super_modulo = mod
        return group

    @staticmethod
    def parse_operation(line: str):
        op = line.replace("Operation: new =", "").replace(" ", "")
        for k, v in operations.items():
            if k in op:
                left, right = op.split(k)
                if left == "old":
                    if right == "old":
                        return lambda x: v(x, x)
                    return lambda x: v(x, int(right))
        raise ValueError(f"cannot parse operation: '{line}'")

    def run(self):
        while self.items:
            self.inspected += 1
            worry = self.items.pop(0)
            worry = self.operation(worry)
            if self.divide:
                worry = int(worry // 3)
            else:
                worry = int(worry % self.group.super_modulo)

            to = self.throw_true if worry % self.divide_by == 0 else self.throw_false
            self.group[to].items.append(worry)

    def __repr__(self) -> str:
        return f"{self.id_}: {self.items}"

    def __str__(self) -> str:
        return repr(self)


def run(group: Group):
    for k, v in group.monkeys.items():
        v.run()


def get_monkey_business(group: Group, rounds=20):
    for _ in range(rounds):
        run(group)
    inspected = sorted((m.inspected for m in group.monkeys.values()), reverse=True)[:2]
    return reduce(operator.mul, inspected)


def run_part_1(puzzle: str):
    group = Monkey.parse_all(puzzle)
    return get_monkey_business(group)


def run_part_2(puzzle: str):
    group = Monkey.parse_all(puzzle, False)
    return get_monkey_business(group, 10000)


if __name__ == "__main__":
    # puzzle = test_data
    puzzle = PuzzleInput(__file__).get()

    print(f"Part 1: {run_part_1(puzzle)}")
    print(f"Part 2: {run_part_2(puzzle)}")
