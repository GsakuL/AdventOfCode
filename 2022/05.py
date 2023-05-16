import copy
import re
from typing import Dict, List, NamedTuple, Optional, Set, TypedDict

from aoc_components import PuzzleInput

def parse_setup(lines: list[str]):
    nums_line: str = lines.pop()
    indexes = []
    stacks: dict[int, list] = {}
    def get_or_add(i):
        stack = stacks.get(i)
        if stack is None:
            stack = []
            stacks[i] = stack
        return stack

    for i, char in enumerate(nums_line):
        if not char.isspace():
            indexes.append((i, int(char)))
    while lines:
        line = lines.pop()
        for i, char in indexes:
            crate = line[i]
            if not crate.isspace():
                get_or_add(char).append(crate)
    return stacks

class Op(NamedTuple):
    number: int
    from_: int
    to: int

exp = re.compile(r"^\s*move (\d+) from (\d+) to (\d+)\s*$")

def parse(txt: str):
    lines = txt.splitlines()
    setup_lines = []
    while True:
        line = lines.pop(0)
        if not line:
            break
        setup_lines.append(line)
    stacks = parse_setup(setup_lines)

    operations: list[Op] = []
    for line in lines:
        m = exp.match(line)
        if not m:
            raise ValueError(m)
        nums = map(int, m.groups())
        operations.append(Op(*nums))
    return stacks, operations

def execute(stacks: dict[int, list], operations: list[Op]):
    for op in operations:
        for _ in range(op.number):
            stacks[op.to].append(stacks[op.from_].pop())

def execute_2(stacks: dict[int, list], operations: list[Op]):
    for op in operations:
        swap = stacks[op.from_][-op.number:]
        stacks[op.from_] = stacks[op.from_][:-op.number]
        stacks[op.to].extend(swap)

if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).get()
    stacks, operations = parse(puzzle)
    stacks_2 = copy.deepcopy(stacks)

    execute(stacks, operations)
    part_1 = "".join((v[-1] for k, v in stacks.items()))
    print(f"Part 1 {part_1}")

    execute_2(stacks_2, operations)
    part_2 = "".join((v[-1] for k, v in stacks_2.items()))
    print(f"Part 2 {part_2}")
