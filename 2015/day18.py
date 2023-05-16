from aoc_components.input_getter import get_my_input
from itertools import product, permutations
from typing import List, Dict, Tuple
from collections import defaultdict, UserDict

inp = get_my_input(__file__)

G = Dict[Tuple[int, int], bool]

directions: List[Tuple[int, int]] = list(product((-1, 0, 1), repeat=2))
directions.remove((0, 0))

corners = ((0, 0), (0, 99), (99, 0), (99, 99))


def get_neighbours(k, current_grid: G):
    global directions
    for d in directions:
        try:
            k_x, k_y = k
            x, y = d
            yield current_grid[(k_x + x, k_y + y)]
        except KeyError:
            pass


def new_value(this: bool, neighbours: List[bool]):
    on = sum(neighbours)
    if this:
        return on in (2, 3)
    return on == 3


def advance(current_grid: G, stuck=False):
    new_grid: G = {}
    for k, v in current_grid.items():
        if stuck and k in corners:
            new_grid[k] = True
            continue
        neighbours = list(get_neighbours(k, current_grid))
        new_grid[k] = new_value(v, neighbours)
    if stuck:
        assert sum((v for k, v in new_grid.items() if k in corners)) == 4
    return new_grid


def main(stuck=False):
    lights: G = {}
    for i, line in enumerate(inp.splitlines()):
        for j, char in enumerate(line):
            lights[(i, j)] = (char == "#")
    if stuck:
        for k in corners:
            lights[k] = True

    for _ in range(100):
        lights = advance(lights, stuck)
    print(sum(lights.values()))
    # test()


if __name__ == "__main__":
    # main()
    main(True)
