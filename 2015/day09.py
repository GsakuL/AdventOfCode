from aoc_components.input_getter import get_my_input
from typing import Dict, Tuple
import itertools
inp = get_my_input(__file__)


def get_total_distance(route: tuple, distances: Dict[Tuple[str, str], int]):
    c = 0
    for i in range(len(route)-1):
        a = route[i]
        b = route[i+1]

        c += distances.get((a, b)) or distances.get((b, a))
    return c


if __name__ == "__main__":
    distances = {}
    locations = set()
    for line in inp.splitlines():
        route, dist = line.split(" = ")
        a, b = route.split(" to ")
        distances[(a, b)] = int(dist)

    for dist in distances:
        locations.add(dist[0])
        locations.add(dist[1])

    print(min((get_total_distance(r, distances) for r in itertools.permutations(locations))))
    print(max((get_total_distance(r, distances) for r in itertools.permutations(locations))))
