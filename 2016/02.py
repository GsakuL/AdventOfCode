from aoc_components import PuzzleInput
from typing import Any, Tuple, List

pad_1 = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
)

pad_2 = (
    ("#", "#", "1", "#", "#"),
    ("#", "2", "3", "4", "#"),
    ("5", "6", "7", "8", "9"),
    ("#", "A", "B", "C", "#"),
    ("#", "#", "D", "#", "#"),
)

movement = {
    "U": (1, -1),
    "D": (1, 1),
    "L": (0, -1),
    "R": (0, 1),
}


def run(puzzle: str, pad: Tuple[Tuple[Any, ...], ...], pos: List[int]):
    mx = len(pad) - 1  # it's square
    code: str = ""
    for line in puzzle.strip().split("\n"):
        for char in line.strip():
            i, d = movement[char]
            pos[i] += d
            if pos[i] < 0:
                pos[i] = 0
            elif pos[i] > mx:
                pos[i] = mx

            button = pad[pos[1]][pos[0]]
            if button == "#":
                pos[i] -= d

        code += str(pad[pos[1]][pos[0]])
    print(code)


def one(puzzle: str):
    return run(puzzle, pad_1, [1, 1])


def two(puzzle: str):
    return run(puzzle, pad_2, [0, 2])


if __name__ == "__main__":
    my = PuzzleInput(__file__).get()
    one(my)
    two(my)
