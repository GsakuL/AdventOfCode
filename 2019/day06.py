from dataclasses import dataclass
from typing import Dict, List

from aoc_components.input_getter import get_my_list

puzzle_input = get_my_list(2019, 6)

example = ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L"]
example2 = ["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L", "K)YOU", "I)SAN"]

@dataclass()
class Orbit:
    center: str
    orbiting: List[str]


def map_orbits(orbits: List[str]):
    map_ = dict()
    for orb in orbits:
        c, o = orb.split(")")
        e = map_.get(c)
        if not e:
            map_[c] = [o]
        else:
            map_[c].append(o)
    return map_


def get_path_length_to_center(map_: Dict[str, List[str]], start: str, current_len=0):
    for k, v in map_.items():
        if start in v:
            return get_path_length_to_center(map_, k, current_len+1)
    return current_len


def count_paths(map_: Dict[str, List[str]]):
    count = 0
    for k, v in map_.items():
        for v_ in v:
            count += get_path_length_to_center(map_, v_)
    return count


def build_path(map_: Dict[str, List[str]], start: str, current_path=None):
    if current_path is None:
        current_path = []
    for k, v in map_.items():
        if start in v:
            return build_path(map_, k, current_path + [k])
    return current_path


def find_first_intersection(a: List[str], b: List[str]):
    same = set(a).intersection(set(b))
    measures = [(s, a.index(s)) for s in same]
    measures = sorted(measures, key=lambda t: t[1])
    return measures[0][0]

def run_example():
    mapping = map_orbits(example)
    count = count_paths(mapping)
    print(count == 42)


def run_part_1():
    mapping = map_orbits(puzzle_input)
    count = count_paths(mapping)
    print(count)


def run_part_2():
    mapping = map_orbits(puzzle_input)
    path_you = build_path(mapping, "YOU")
    path_san = build_path(mapping, "SAN")
    inter = find_first_intersection(path_you, path_san)
    intersection_you = path_you.index(inter)
    intersection_san = path_san.index(inter)
    print(intersection_you + intersection_san)

run_part_2()
