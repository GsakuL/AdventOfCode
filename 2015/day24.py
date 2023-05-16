from aoc_components.puzzle_input import PuzzleInput


class Stop(Exception):
    pass


def run2(result: list, a: list, b: list, c: list, left_over: list, max_per: int, it=0):

    t = a, b, c
    s = [sum(x) for x in t]

    if any((_ > max_per for _ in s)):
        return
    elif all((_ == max_per for _ in s)):
        result.append(t)
        return
    else:

        # a, b, c = a[:], b[:], c[:]

        for x in left_over:
            run2(result, a+[x], b, c, ex(left_over, x), max_per, it+1)
            run2(result, a, b+[x], c, ex(left_over, x), max_per, it+1)
            run2(result, a, b, c+[x], ex(left_over, x), max_per, it+1)


def run(result: list, used: list, left_over: list, max_per: int, it=0):
    s = sum(used)
    if s == max_per:
        result.append(used)
        r1 = []
        run(r1, [], left_over, max_per)
    elif s < max_per:  # and can_advance(used):
        for i, x in enumerate(left_over):
            try:
                # run(result, used + [x], ex(left_over, x), max_per, it+1)
                run(result, used + [x], left_over[i+1:], max_per, it+1)
            except Stop:
                pass
    else:
        raise Stop(it)


def ex(lst: list, i: int):
    return [x for x in lst if x != i]


def can_advance(used: list):
    return (len(used) < 2) or (used[-1] < used[-2])


if __name__ == "__main__":
    inp = PuzzleInput(__file__).get()
    #weights = sorted((int(line) for line in inp.splitlines()), reverse=True)
    weights = [11, 9, 10, 8, 2, 7, 5, 4, 3, 1]
    max_per = sum(weights) / 3
    result = []
    L = run(result, [], weights, max_per)
    #L = run2(result, [], [], [], weights, max_per)
    print()
    # print(f"Part 1: {run([], weights, max_per)}")

    # print(f"Part 2: {run(inp, 1)}")
