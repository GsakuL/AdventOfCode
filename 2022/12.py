from __future__ import annotations

import operator
import os
import re
from dataclasses import dataclass
from math import hypot
from typing import Callable, Dict, List, NamedTuple, Optional, Protocol, Set, TypedDict

from colorama import Back, Fore, Style, just_fix_windows_console

from aoc_components import PuzzleInput


class Pos(NamedTuple):
    x: int
    y: int
    h: int = 0

    def _calc(self, other: 'Pos', op):
        return Pos(op(self.x, other.x), op(self.y, other.y), op(self.h, other.h))

    def __add__(self, other: 'Pos'):
        return self._calc(other, operator.add)

    def __sub__(self, other: 'Pos'):
        return self._calc(other, operator.sub)

    def get_distance(self, other: 'Pos'):
        a = abs(self.x - other.x)
        b = abs(self.y - other.y)
        c = abs(self.h - other.h)
        return int(hypot(a, b, c) * 100)


class Cost(NamedTuple):
    target_cost: int
    origin_cost: int

    @property
    def total_cost(self):
        return self.origin_cost + self.target_cost

    def key(self):
        return (self.total_cost, self.target_cost)


MAX_COST = Cost(float('inf'), float('inf'))
ZERO_COST = Cost(0, 0)


@dataclass
class Node:
    letter: str
    pos: Pos
    cost: Cost | None = None
    parent: 'Node' | None = None
    is_result = False

    def key(self):
        return (self.cost or MAX_COST).key()

    def can_go_to(self, other: 'Node'):
        diff = other.pos - self.pos
        return abs(diff.x) + abs(diff.y) == 1 and diff.h <= 1


def calculate_cost(previous: Node, current: Pos | Node, target: Pos | Node, target_cost: None | int = None):
    if isinstance(current, Node):
        current = current.pos
    if isinstance(target, Node):
        target = target.pos
    if target_cost is None:
        target_cost = current.get_distance(target)
    return Cost(target_cost, current.get_distance(previous.pos) + (previous.cost or ZERO_COST).origin_cost)


class Special(NamedTuple):
    Start: Node
    End: Node


class Map(NamedTuple):
    grid: list[list[Node]]
    special: Special


Grid = list[list[Node]]

DIRECTIONS = (Pos(0, 1), Pos(0, -1), Pos(1, 0), Pos(-1, 0))


@dataclass
class Result:
    open_nodes: list[Node]
    closed_nodes: list[Node]
    final_node: Node | None = None

    def mark_done(self):
        if not self.final_node:
            raise TypeError()
        current = self.final_node
        count = -1
        while current:
            count += 1
            current.is_result = True
            current = current.parent
        return count


def print_fancy(current: Node, map_: Map, result: Result):
    buffer = f"{Back.BLACK}"
    print()
    for line in map_.grid:
        for pos in line:
            color = Fore.WHITE
            style = Style.NORMAL
            if current == pos:
                color = Fore.CYAN
                style = Style.BRIGHT
            if pos in result.closed_nodes:
                color = Fore.RED
            if pos in result.open_nodes:
                color = Fore.GREEN
            if pos.is_result:
                color = Fore.YELLOW
            if pos == map_.special.Start:
                color = Fore.BLUE
            if pos == map_.special.End:
                color = Fore.BLUE
            buffer += f"{style}{color}{pos.letter}"
        buffer += "\n"
    buffer += f"{Style.RESET_ALL}{Fore.RESET}{Back.RESET}"
    print(buffer.strip())


def get_height(char: str):
    if char == "S":
        char = "a"
    if char == "E":
        char = "z"
    return ord(char) - ord('a')


def parse(puzzle: str):
    grid = Grid()
    for i, line in enumerate(puzzle.splitlines()):
        row = []
        for j, char in enumerate(line):
            pos = Node(char, Pos(j, i, get_height(char)), None)
            row.append(pos)
            if char == "S":
                start = pos
            if char == "E":
                end = pos
        grid.append(row)
    return Map(grid, Special(start, end))


def get_from_list(obj: list, index: int):
    if 0 <= index < len(obj):
        return obj[index]
    raise KeyError(index)


NodeTest = Callable[[Node, Node], bool]


def resolve(map_: Map, start: Node, end: Node, traversable: NodeTest, is_end: NodeTest, target_cost: int | None):
    open_nodes = [start]
    closed_nodes = list[Node]()
    result = Result(open_nodes, closed_nodes)

    while True:
        open_nodes.sort(key=lambda x: x.key())
        current = open_nodes[0]
        open_nodes.remove(current)
        closed_nodes.append(current)
        if is_end(current, end):
            result.final_node = current
            return result

        for di in DIRECTIONS:
            diff = di + current.pos
            try:
                neighbour: Node = get_from_list(get_from_list(map_.grid, diff.y), diff.x)
            except KeyError:
                continue
            if (not traversable(current, neighbour)) or neighbour in closed_nodes:
                continue
            new_cost = calculate_cost(current, neighbour, end, target_cost)
            if (not neighbour.cost) or (new_cost.total_cost < neighbour.cost.total_cost) or neighbour not in open_nodes:
                neighbour.cost = new_cost
                neighbour.parent = current
                if neighbour not in open_nodes:
                    open_nodes.append(neighbour)


def is_end_pos(current: Node, end: Node):
    return current.pos == end.pos


def is_an_a(current: Node, end: Node):
    _ = end
    return current.letter == "a"


def resolve_forward(map_: Map, is_end: NodeTest, target_cost: int | None):
    return resolve(map_, map_.special.Start, map_.special.End, lambda x, y: x.can_go_to(y), is_end, target_cost)


def resolve_backwards(map_: Map, is_end: NodeTest, target_cost: int | None):
    return resolve(map_, map_.special.End, map_.special.Start, lambda x, y: y.can_go_to(x), is_end, target_cost)


TEST_PUZZLE = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def part_1(puzzle: str):
    map_ = parse(puzzle)
    # result = resolve_forward(map_, is_end_pos, None)
    result = resolve_backwards(map_, is_end_pos, None)
    count = result.mark_done()
    print_fancy(None, map_, result)
    print(f"Part 1: Steps={count}")


def part_2(puzzle: str):
    map_ = parse(puzzle)
    # result = resolve_forward(map_, is_an_a, 0)
    result = resolve_backwards(map_, is_an_a, 0)
    count = result.mark_done()
    print_fancy(None, map_, result)
    print(f"Part 2: Steps={count}")


def main():
    just_fix_windows_console()
    puzzle = PuzzleInput(__file__).get()
    # puzzle = TEST_PUZZLE
    # part_1(puzzle)
    part_2(puzzle)


if __name__ == "__main__":
    main()
