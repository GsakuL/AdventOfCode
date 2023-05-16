from aoc_components.input_getter import get_my_input
from typing import Dict, Tuple
import itertools
from collections import defaultdict

inp = get_my_input(__file__)


def get_total_likings(sitting: tuple, likings: Dict[Tuple[str, str], int]):
    c = 0
    s = len(sitting)
    for i in range(s-1):
        a = sitting[i]
        b = sitting[i+1]
        c += likings[(a, b)] + likings[(b, a)]
    a = sitting[s-1]
    b = sitting[0]
    c += likings[(a, b)] + likings[(b, a)]
    return c


if __name__ == "__main__":
    likings = defaultdict(int)
    people = set()
    for line in inp.splitlines():
        x, B = line.split(" happiness units by sitting next to ")
        B = B.strip(".")
        A, g = x.split(" would ")
        G, V = g.split(" ")
        V = int(V)
        if G == "lose":
            V = 0-V
        likings[(A, B)] = int(V)

    for dist in likings:
        people.add(dist[0])
        people.add(dist[1])

    def get():
        return max(
            (get_total_likings(r, likings)
             for r
             in itertools.permutations(people))
            )

    print(get())
    people.add("Me")
    print(get())
