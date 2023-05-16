import re
from typing import Dict, List, NamedTuple, Optional, Set, Tuple, TypedDict

from aoc_components import PuzzleInput

example_data_1 = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""


class HGC:

    def __init__(self, code: List[Tuple[str, int]]) -> None:
        self.pointer = 0
        self.accumulator = 0
        self.code = code
        self.order = []
        self.looped = False
        self.done = False
        self.changed = -1

    @staticmethod
    def parse(code: str):
        lines = [(i, int(val)) for i, val in (line.split(" ")
                                              for line in code.splitlines()
                                              if line)]
        return HGC(lines)

    def _step(self):
        self.order.append(self.pointer)
        instruction, val = self.code[self.pointer]
        if instruction == "jmp":
            self.pointer += val
        if instruction == "nop":
            self.pointer += 1
        if instruction == "acc":
            self.accumulator += val
            self.pointer += 1

    def step(self) -> Optional["HGC"]:
        if self.pointer in self.order:
            self.looped = True
            return self
        if self.pointer >= len(self.code):
            self.done = True
            return self
        self._step()

    def run(self) -> "HGC":
        result = None
        while result is None:
            result = self.step()
        return result

    def copy(self) -> "HGC":
        return HGC([(ins, val) for ins, val in self.code])

    def replace(self, index: int):
        ins, val = self.code[index]
        if ins == "nop":
            ins = "jmp"
        elif ins == "jmp":
            ins = "nop"
        else:
            raise RuntimeError(f"wont change {ins}")
        self.code[index] = (ins, val)
        self.changed = index
        return self

    def get_permuations(self):
        for i, code in enumerate(self.code):
            if code[0] in ("jmp", "nop"):
                yield self.copy().replace(i)


def part_2(base: HGC, debug=False):
    for i, perm in enumerate(my.get_permuations()):
        if debug:
            print(f"\t{i}:\t{perm.changed}")
        perm.run()
        if perm.done:
            return perm
    raise RuntimeError("no permutation found")


if __name__ == "__main__":

    example_1 = HGC.parse(example_data_1).run()

    assert example_1.accumulator == 5

    puzzle = PuzzleInput(__file__)()
    my = HGC.parse(puzzle).run()
    print(f"{my.accumulator=}")

    part2 = part_2(my)

    print(f"{part2.accumulator=}")
