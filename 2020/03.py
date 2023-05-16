from aoc_components import PuzzleInput
from aoc_components.utils.wrap_map import WrapMap, Vector2
import functools as ft
from operator import mul


def travel_all(wrap: WrapMap):
    return [
        travel(wrap, t[0], t[1])
        for t in
        [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    ]


def travel(wrap: WrapMap, d_x: int, d_y: int):
    x = y = 0
    trees = 0
    while y <= wrap.size.y-1:
        current = wrap[Vector2(x, y)]
        if current == "#":
            trees += 1
        x += d_x
        y += d_y
    return (trees, d_x, d_y)


if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).as_list("\n")
    wrap = WrapMap(puzzle)
    traveled = travel_all(wrap)
    print(f"first = {traveled[1]}")
    second = ft.reduce(mul, (t[0] for t in traveled))
    print(f"{second=}")
