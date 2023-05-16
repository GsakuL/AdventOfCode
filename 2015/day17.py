from aoc_components.input_getter import get_my_input
from itertools import combinations
from typing import List
from collections import defaultdict

inp = get_my_input(__file__)


def calc(L: int, buckets: List[int]):
    counter = defaultdict(int)

    min_buckets = 1
    s = sorted(buckets, reverse=True)
    while sum(s[:min_buckets]) < L:
        min_buckets += 1

    max_buckets = len(buckets)
    s = sorted(buckets)
    while sum(s[:max_buckets]) > L:
        max_buckets -= 1
    max_buckets += 1

    for i in range(min_buckets, max_buckets+1):
        combos = combinations(buckets, i)
        for perm in combos:
            if sum(perm) == L:
                counter[len(perm)] += 1

    print(sum(counter.values()))
    mi = min(counter.keys())
    print(counter[mi])


def main():
    buckets = []
    for line in inp.splitlines():
        buckets.append(int(line))

    calc(150, buckets)


def test():
    buckets = [20, 15, 10, 5, 5]
    calc(25, buckets)


if __name__ == "__main__":
    main()
    # test()
