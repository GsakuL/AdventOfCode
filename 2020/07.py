from aoc_components import PuzzleInput

from typing import Dict, NamedTuple, Sequence, Set, TypedDict, Optional, List, Any
import re

example_data1 = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""
example_data2 = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""


class Baggage(NamedTuple):
    count: int
    color: str

    @staticmethod
    def parse(line: str) -> "Baggage":
        count, color = re.sub(r" bags?$", "", line).split(" ", 1)
        return Baggage(int(count), color)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.count}, {self.color})"


BAGS = Dict[str, Set[str]]
BAGS2 = Dict[str, Sequence[Baggage]]

WANTED = "shiny gold"


def add(dic: dict, key: str, value: Any):
    current = dic.get(key)
    if current is None:
        current = set()
        dic[key] = current
    current.add(value)


def generate_bag_graph(data: str):
    bags_inside_out: BAGS = {}
    bags_outside_in: BAGS2 = {}
    for line in data.splitlines():
        if not line or "no other bag" in line:
            continue
        parent, child = line.split(" bags contain ")
        children = [Baggage.parse(c) for c in child.strip(".").split(", ")]
        for baggage in children:
            add(bags_inside_out, baggage.color, parent)
            add(bags_outside_in, parent, baggage)

    return bags_inside_out, bags_outside_in


def go_up(inside_out: BAGS, key: str = WANTED):
    children = inside_out.get(key)
    if not children:
        yield key
        return
    if key == WANTED:
        yield from children
    for c in children:
        yield c
        yield from go_up(inside_out, c)


def count_in(outside_in: BAGS2, key: str = WANTED, running=1):
    children = outside_in.get(key)

    yield 1
    if not children:
        return
    for c in children:
        for sub in count_in(outside_in, c.color):
            yield sub * c.count


def solve(data: str):
    part1, part2 = generate_bag_graph(data)
    outsides = set(go_up(part1))
    count = sum(count_in(part2)) - 1
    return len(outsides), count


if __name__ == "__main__":

    assert solve(example_data1) == (4, 32)
    assert solve(example_data2)[1] == 126

    puzzle = PuzzleInput(__file__)()

    part1, part2 = solve(puzzle)
    print(f"{part1=}")
    print(f"{part2=}")
