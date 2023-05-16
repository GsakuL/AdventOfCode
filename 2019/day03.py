from typing import List, Tuple

from aoc_components.input_getter import get_my_input

puzzle_input = get_my_input(2019, 3)

puzzle_input_a, puzzle_input_b = [_.split(",") for _ in puzzle_input.split("\n")]

demo_1_a = "R8,U5,L5,D3".split(",")
demo_1_b = "U7,R6,D4,L4".split(",")

demo_2_a = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(",")
demo_2_b = "U62,R66,U55,R34,D71,R55,D58,R83".split(",")


positions_a = [(0, 0)]
positions_b = [(0, 0)]


def add_(a: Tuple[int, int], b: Tuple[int, int]):
    return a[0] + b[0], a[1] + b[1]


directions = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


def calc_path(wire: List[str], positions: List[Tuple[int, int]]):
    for vec in wire:
        dir_ = vec[0]
        length = int(vec[1:])
        for _ in range(length):
            positions.append(add_(positions[-1], directions[dir_]))


def get_crossings(w_a: List[Tuple[int, int]], w_b: List[Tuple[int, int]]):
    a = set(w_a)
    b = set(w_b)
    intersections = a.intersection(b)
    intersections.remove((0, 0))
    return intersections


def closest(intersections: List[Tuple[int, int]]):

    distances = [abs(a) + abs(b) for a, b in intersections]
    return min(distances)


def run_(a, b, solution=None):
    pos_a = positions_a.copy()
    pos_b = positions_b.copy()

    calc_path(a, pos_a)
    calc_path(b, pos_b)
    inters_ = list(get_crossings(pos_a, pos_b))
    res = closest(inters_)
    if solution:
        print(f"got: {res} expected: {solution}")
    else:
        print(f"solution = {res}")


def fastest(inters_, pos_a, pos_b):
    distances = [pos_a.index(i) + pos_b.index(i) for i in inters_]
    return min(distances)


def run_2(a, b, solution=None):
    pos_a = positions_a.copy()
    pos_b = positions_b.copy()

    calc_path(a, pos_a)
    calc_path(b, pos_b)
    inters_ = list(get_crossings(pos_a, pos_b))
    res = fastest(inters_, pos_a, pos_b)

    if solution:
        print(f"got: {res} expected: {solution}")
    else:
        print(f"solution = {res}")


def part_1():
    run_(demo_1_a, demo_1_b, 6)
    run_(demo_2_a, demo_2_b, 159)
    run_(puzzle_input_a, puzzle_input_b)


def part_2():
    run_2(demo_1_a, demo_1_b, 30)
    run_2(demo_2_a, demo_2_b, 610)
    run_2(puzzle_input_a, puzzle_input_b)

part_2()