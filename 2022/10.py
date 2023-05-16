import re
from typing import Dict, List, NamedTuple, Optional, Sequence, Set, TypedDict

from aoc_components import PuzzleInput
from aoc_components.validate import Validate

test_data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

test_crt_result = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""

BLOCK = "█"
LIGHT = "░"
EMPTY = " "


class Crt:
    WIDTH = 40
    HEIGHT = 6

    def __init__(self, block: str | None = None, empty: str | None = None) -> None:
        self._pixels = [[0] * Crt.WIDTH for _ in range(Crt.HEIGHT)]
        self._x = 0
        self._y = 0
        self._block = BLOCK if block is None else block
        self._empty = EMPTY if empty is None else empty

    def clock_step(self, cpu: 'Cpu'):
        self._pixels[self._y][self._x] = abs(cpu.x - self._x) <= 1
        self._x += 1
        if self._x == Crt.WIDTH:
            self._x = 0
            self._y += 1
        if self._y == Crt.HEIGHT:
            self._y = 0

    def draw(self):
        return "\n".join("".join((self._block if p else self._empty for p in row)) for row in self._pixels)


class Cpu:

    def __init__(self, crt: Crt) -> None:
        self._cycles = 0
        self._x = 1
        self._queue = []
        self._crt = crt

    @property
    def cycles(self):
        return self._cycles

    @property
    def x(self):
        return self._x

    @property
    def crt(self):
        return self._crt

    def _clock_step(self):
        self._cycles += 1
        self._crt.clock_step(self)

    def __noop(self):
        self._clock_step()

    def noop(self):
        self._queue.append(self.__noop)

    def __addx(self, value: int):
        self._x += value

    def addx(self, value: int):
        self.noop()
        self.noop()
        self._queue.append(lambda: self.__addx(value))

    def step(self):
        if self._queue:
            op = self._queue.pop(0)
            op()
            return True
        return False

    def parse_line(self, line: str):
        if line == "noop":
            self.noop()
        else:
            cmd, arg = line.split()
            if cmd == "addx":
                self.addx(int(arg))
            else:
                raise RuntimeError(f"unknown instruction {line}")

    def parse_lines(self, lines: Sequence[str]):
        for line in lines:
            self.parse_line(line)


def run(cpu: Cpu):
    wanted = 20
    signals = []
    while True:
        if wanted == cpu.cycles:
            signals.append(cpu.x * cpu.cycles)
        if wanted <= cpu.cycles:
            wanted += 40

        if not cpu.step():
            break
    return signals


def run_tests():
    cpu = Cpu(Crt("#", "."))
    cpu.parse_lines(test_data.splitlines())
    signals = run(cpu)

    Validate.equals(sum(signals), 13140)
    Validate.equals(cpu.crt.draw(), test_crt_result)
    print("test ok")


if __name__ == "__main__":
    run_tests()

    puzzle = PuzzleInput(__file__).get()
    cpu = Cpu(Crt())
    cpu.parse_lines(puzzle.splitlines())

    signals = run(cpu)

    # 174 too low
    # 20440 too high
    print(f"Part 1 {sum(signals)}")

    result = cpu.crt.draw()

    # assert result == test_crt_result
    # print("\n\n" + test_crt_result + "\n\n")
    print(f"Part 2:\n\n{result}")
