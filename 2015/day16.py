from aoc_components.input_getter import get_my_input
from operator import eq, lt, gt
import re
inp = get_my_input(__file__)


keys_eq = (
    "children",
    "samoyeds",
    "akitas",
    "vizslas",
    "cars",
    "perfumes",
)

keys_gt = (
    "cats",
    "trees",
)

keys_lt = (
    "pomeranians",
    "goldfish",
)

r = re.compile(r"Sue (\d+): (.+)")

sample = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def parse(line: str) -> dict:
    global r
    m = r.match(line)
    if not m:
        raise RuntimeError()
    aunt = {
        "id": m[1]
    }
    pairs = m[2]
    for pair in pairs.split(", "):
        k, v = pair.split(": ")
        aunt[k] = int(v)
    return aunt


def match_(a, b, op):
    return (b is None or op(b, a))


def may_match_1(aunt: dict):
    global keys_eq
    global sample
    for keys, op in ((keys_eq, eq), (keys_gt, eq), (keys_lt, eq)):
        for k in keys:
            a = sample[k]
            b = aunt.get(k)
            if not match_(a, b, op):
                return False
    return True


def may_match_2(aunt: dict):
    global keys_eq
    global sample
    for keys, op in ((keys_eq, eq), (keys_gt, gt), (keys_lt, lt)):
        for k in keys:
            a = sample[k]
            b = aunt.get(k)
            if not match_(a, b, op):
                return False
    return True


def main():
    aunts = []
    for line in inp.splitlines():
        aunts.append(parse(line))

    possible = [a for a in aunts if may_match_1(a)]
    assert len(possible) == 1
    print(possible[0]["id"])

    possible = [a for a in aunts if may_match_2(a)]
    assert len(possible) == 1
    print(possible[0]["id"])


if __name__ == "__main__":
    main()
