from aoc_components import PuzzleInput
import re


def is_possible(a: int, b: int, c: int):
    return (a + b > c and a + c > b and b + c > a)


def one(puzzle: str):
    space = re.compile(r"\s+")
    possible = 0
    for line in puzzle.split("\n"):
        a, b, c = (int(n) for n in space.split(line.strip()))
        possible += is_possible(a, b, c)
    print(f"possible: {possible}")


def two(puzzle: str):
    space = re.compile(r"\s+")
    possible = 0
    lines = puzzle.split("\n")
    for i in range(0, len(lines), 3):
        a_x, a_y, a_z = (int(n) for n in space.split(lines[i + 0].strip()))
        b_x, b_y, b_z = (int(n) for n in space.split(lines[i + 1].strip()))
        c_x, c_y, c_z = (int(n) for n in space.split(lines[i + 2].strip()))
        possible += (is_possible(a_x, b_x, c_x) + is_possible(a_y, b_y, c_y) + is_possible(a_z, b_z, c_z))
    print(f"possible: {possible}")


if __name__ == "__main__":
    my = PuzzleInput(__file__).get()
    one(my)
    two(my)