from aoc_components.input_getter import get_my_input
from itertools import product, permutations
from typing import List, Dict, Tuple, NamedTuple
from collections import defaultdict, UserDict
import re
from random import shuffle
inp = get_my_input(__file__)


class Mutation(NamedTuple):
    from_: str
    to: str


def main():
    pass


def reverse(mutations: List[Mutation], molecule: str):
    i = 0
    n = len(mutations)
    while i < n and molecule != "e":
        m = mutations[i]
        new = molecule.replace(m.to, m.from_)
        if new == molecule:
            i += 1
        else:
            i = 0
        molecule = new
    return molecule


class DeadEnd(Exception):
    pass


def reverse2(mutations: List[Mutation], molecule: str, steps=0):
    if molecule == "e":
        yield steps
    for mut in mutations:
        for m in re.finditer(mut.to, molecule):
            new = molecule[:m.start()] + mut.from_ + molecule[m.end():]
            try:
                yield next(reverse2(mutations, new, steps+1))
            except DeadEnd:
                pass
    if steps > 0:
        raise DeadEnd()


def reverse3(mutations: List[Mutation], molecule: str):
    steps = 0
    while molecule != "e":
        for mut in mutations:
            if mut.to in molecule:
                steps += 1
                molecule = molecule.replace(mut.to, mut.from_, 1)

    return steps


def cheat():
    import re

    molecule = inp.split('\n')[-1][::-1]
    reps = {m[1][::-1]: m[0][::-1]
            for m in re.findall(r'(\w+) => (\w+)', inp)}
    def rep(x):
        return reps[x.group()]

    count = 0
    while molecule != 'e':
        molecule = re.sub('|'.join(reps.keys()), rep, molecule, 1)
        count += 1

    print(count)


if __name__ == "__main__":
    mutations: List[Mutation] = []
    for line in inp.splitlines():
        if not line:
            continue
        if "=>" in line:
            f, t = line.split(" => ")
            mutations.append(Mutation(f, t))
        else:
            medicine = line.strip()

    def key_(m: Mutation):
        return (len(m.to), len(m.from_))

    mutations_ = sorted(mutations, key=key_)
    mutations_r = sorted(mutations, key=key_, reverse=True)
    molecules = set()

    for mut in mutations:
        for m in re.finditer(mut.from_, medicine):
            new = medicine[:m.start()] + mut.to + medicine[m.end():]
            molecules.add(new)
    # print(len(molecules))

    # revs = list(reverse2(mutations, medicine))
    # print(reverse(mutations, medicine))
    #shuffle(mutations)
    #print(reverse3(mutations, medicine))
    cheat()
