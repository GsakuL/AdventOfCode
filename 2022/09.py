import operator
from typing import Callable, NamedTuple

from aoc_components import PuzzleInput


class Pos(NamedTuple):
    x: int
    y: int

    def _alter(self, other, op: Callable[[int, int], int]):
        if not isinstance(other, Pos):
            return NotImplemented
        return Pos(op(self.x, other.x), op(self.y, other.y))

    def __add__(self, other):
        return self._alter(other, operator.add)

    def __mul__(self, other):
        return self._alter(other, operator.mul)


class Move(NamedTuple):
    direction: Pos
    steps: int


directions = {
    "U": Pos(0, 1),
    "D": Pos(0, -1),
    "R": Pos(1, 0),
    "L": Pos(-1, 0),
}


def parse(txt: str):
    moves: list[Move] = []
    for line in txt.splitlines():
        d, steps = line.split()
        moves.append(Move(directions[d], int(steps)))
    return moves


def follow(tail: Pos, head: Pos) -> Pos:
    x_diff = head.x - tail.x
    y_diff = head.y - tail.y
    if abs(x_diff) <= 1 and abs(y_diff) <= 1:
        return tail

    if head.x == tail.x:
        step = Pos(0, 1)
    elif head.y == tail.y:
        step = Pos(1, 0)
    else:
        step = Pos(1, 1)

    if x_diff < 0:
        step *= Pos(-1, 1)
    if y_diff < 0:
        step *= Pos(1, -1)

    return tail + step


def walk(moves: list[Move], knots=1):
    head = Pos(0, 0)
    rope = [Pos(0, 0) for _ in range(knots)]
    board = {head}

    for move in moves:
        for _ in range(move.steps):
            head += move.direction
            for i in range(knots):
                prev = head if i == 0 else rope[i - 1]
                rope[i] = follow(rope[i], prev)
            board.add(rope[-1])

    return board


if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).get()
    moves = parse(puzzle)

    board = walk(moves)
    print(f"Part 1: {len(board)}")

    board_2 = walk(moves, 9)
    print(f"Part 2: {len(board_2)}")
