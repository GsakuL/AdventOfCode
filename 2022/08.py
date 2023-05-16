import operator
from functools import reduce

from aoc_components import PuzzleInput

Puzzle = list[list[int]]

test_data = """30373
25512
65332
33549
35390"""

HEADINGS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def parse(puzzle: str) -> Puzzle:
    return [[int(c) for c in line] for line in puzzle.splitlines()]


def is_visible_in_direction(tree: int, heading: tuple[int, int], x: int, y: int, puzzle: Puzzle, h: int, w: int):
    while True:
        x = x + heading[0]
        y = y + heading[1]
        if (x in (-1, w)) or (y in (-1, h)):
            return True
        if puzzle[x][y] >= tree:
            return False


def is_visible(x: int, y: int, puzzle: Puzzle, h: int, w: int):
    tree = puzzle[x][y]
    for heading in HEADINGS:
        if is_visible_in_direction(tree, heading, x, y, puzzle, h, w):
            return True
    return False


def count_visible(puzzle: Puzzle):
    h = len(puzzle)
    w = len(puzzle[0])
    count = 0
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            if is_visible(x, y, puzzle, h, w):
                count += 1
    count += (h + (w - 2)) * 2
    return count


def get_score_in_direction(tree: int, heading: tuple[int, int], x: int, y: int, w: int, h: int, puzzle: Puzzle):
    count = 0
    while True:
        x = x + heading[0]
        y = y + heading[1]
        if (x in (-1, w)) or (y in (-1, h)):
            break
        count += 1
        if puzzle[x][y] >= tree:
            break
    return count


def get_score_for_tree(x: int, y: int, w: int, h: int, puzzle: Puzzle):
    tree = puzzle[x][y]
    return reduce(operator.mul, (get_score_in_direction(tree, heading, x, y, w, h, puzzle) for heading in HEADINGS))


def get_score(puzzle: Puzzle):
    h = len(puzzle)
    w = len(puzzle[0])
    best = 0
    for x in range(w):
        for y in range(h):
            best = max(best, get_score_for_tree(x, y, w, h, puzzle))
    return best


if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).get()
    grid = parse(puzzle)

    c = count_visible(grid)
    print(f"Part 1: {c}")

    score = get_score(grid)
    print(f"Part 2: {score}")
