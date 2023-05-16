from aoc_components import PuzzleInput
from typing import NamedTuple, Set, Tuple


class Step(NamedTuple):
    direction: str
    steps: int


def parse(puzzle: str):
    return [Step(j[0], int(j[1:])) for j in puzzle.split(", ")]


movement = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}


def turn(current: int, rot: str):
    current += (1 if rot == "R" else -1)
    if current < 0:
        current += 4
    if current > 3:
        current -= 4
    return current


def one(puzzle: str):
    pos = [0, 0]
    current = 0
    for s in parse(puzzle):
        current = turn(current, s.direction)
        mov = movement[current]
        for i in range(2):
            pos[i] += mov[i] * s.steps

    print(f"end: {pos}")
    print(sum(abs(p) for p in pos))


def two(puzzle: str):
    first = None
    visited: Set[Tuple[int, ...]] = {(0, 0)}
    pos = [0, 0]
    current = 0
    try:
        for s in parse(puzzle):
            current = turn(current, s.direction)
            mov = movement[current]
            for _ in range(s.steps):
                for i in range(2):
                    pos[i] += mov[i]
                _pos = tuple(pos)
                if _pos in visited:
                    first = _pos
                    raise StopIteration()
                else:
                    visited.add(_pos)
    except StopIteration:
        pass

    print(f"\nfirst twice: {first}")
    print(sum(abs(p) for p in first or (0, 0)))


if __name__ == "__main__":
    my = PuzzleInput(__file__).get()
    one(my)
    two(my)
