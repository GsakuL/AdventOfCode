from collections import Counter
from multiprocessing.pool import Pool
from typing import List, Tuple

from aoc_components.input_getter import get_my_input
from aoc_components.int_code_computer import IntCodeComputer
from aoc_components.screen import Screen, Transform

puzzle_input = get_my_input(2019, 17)


def get_tiles_around(x, y, screen_: Screen):
    return (
        ((x + 1, y), screen_[(x + 1, y)]),
        ((x - 1, y), screen_[(x - 1, y)]),
        ((x, y + 1), screen_[(x, y + 1)]),
        ((x, y - 1), screen_[(x, y - 1)])
    )


def mark_intersections(screen_: Screen) -> set:
    def _is_intersection(x, y):
        return all((_[1] == "#" for _ in get_tiles_around(x, y, screen_)))
    i = set()

    for k, v in list(screen_.pixels.items()):
        if v == "#" and _is_intersection(*k):
            screen_[k] = "O"
            i.add(k)
    return i



def part_1():
    x = y = 0
    screen_ = Screen(default=None)
    def _out(a):
        nonlocal x, y
        a = chr(a)
        if a in ("\n", "\r"):
            x = -1
            y -= 1
        else:
            screen_[(x, y)] = a
        print(a, end="")
        x += 1
    proc = IntCodeComputer(puzzle_input, output_consumer=_out)
    proc.run()
    i = mark_intersections(screen_)
    screen_.paint()
    s1_ = sum((abs(_[0])*abs(_[1]) for _ in i))
    return screen_, s1_


UP = "^"
RIGHT = ">"
DOWN = "V"
LEFT = "<"


def construct_path(screen_: Screen):
    dir_ = UP

    def get_rotation(p2):
        nonlocal dir_
        x_ = p2[0] - x
        y_ = p2[1] - y
        is_ = (dir_, x_, y_)

        if is_ == (UP, 1, 0):
            return "R", RIGHT
        if is_ == (UP, -1, 0):
            return "L", LEFT
        if is_ == (RIGHT, 0, -1):
            return "R", DOWN
        if is_ == (RIGHT, 0, 1):
            return "L", UP
        if is_ == (DOWN, 1, 0):
            return "L", RIGHT
        if is_ == (DOWN, -1, 0):
            return "R", LEFT
        if is_ == (LEFT, 0, -1):
            return "L", DOWN
        if is_ == (LEFT, 0, 1):
            return "R", UP

    def find_next(last_=None):
        t = [_ for _ in get_tiles_around(x, y, screen_) if _[1] == "#" and _[0] != last_]
        if len(t) > 1:
            raise ValueError(f"too many options: {t}")
        elif len(t) == 1:
            return t[0][0]
        return None
    p = []
    x, y = next(screen_.find("^"))[0]
    is_done = False
    n = find_next(None)
    r, dir_ = get_rotation(n)
    p.append(r)
    while n:
        dx = n[0] - x
        dy = n[1] - y
        i = 0
        while screen_[(x + ((i + 1) * dx), y + ((i + 1) * dy))] in ("#", "O"):
            i += 1
            p.append("1")
        #p.append(str(i))
        last = (x + ((i-1) * dx), y + ((i-1) * dy))
        x += i * dx
        y += i * dy
        n = find_next(last)
        if n:
            r, dir_ = get_rotation(n)
            p.append(r)
    #p_ = find_pattern(p)
    p_ = None
    p_r = mt(p)
    pass
    return p_


def compact(a: str):
    o = []
    i = 0
    for _ in a.split(","):
        if _ == '1':
            i += 1
        else:
            if i:
                o.append(str(i))
                i = 0
            o.append(_)
    if i:
        o.append(str(i))
    return ",".join(o)


def is_completable(a, b, c, p):
    Counter(a)
    p_ = p
    reps = []
    moves = (("A", a, len(a)), ("B", b, len(b)), ("C", c, len(c)))
    found = True
    while len(p_) > 0 and found:
        found = False
        for name, opt, length in moves:
            if p_.startswith(opt):
                reps.append(name)
                p_ = (p_[length:]).strip(",")
                found = True
    if len(p_) > 0:
        return None
    else:
        _a = compact(a)
        _b = compact(b)
        _c = compact(c)
        if len(_a) <= 20 and len(_b) <= 20 and len(_c) <= 20:
            return reps
    return None


def find_pattern(path_: List[str]):
    skip = True
    p = ",".join(path_)
    p__ = compact(p)
    lp = len(path_)
    for al in range(1, lp + 1): #24
        for bl in range(1, lp + 1):
            for cl in range(1, lp + 1):
                print(f"\rcurrently testing for {al, bl, cl}", end="")
                a = ",".join(path_[0:al])
                b = ",".join(path_[al:al+bl])
                c = ",".join(path_[al+bl:al+bl+cl])
                compact(c)
                if skip or (len(a) <= 20 and len(b) <= 20 and len(c) <= 20):
                    sol = is_completable(a, b, c, p)
                    if sol:
                        return ",".join(sol), a, b, c
    return None


def find_pattern_mt(p: Tuple[List[str], int]):
    path_, al = p
    skip = True
    p = ",".join(path_)
    p__ = compact(p)
    lp = len(path_)
    for bl in range(1, lp + 1):
        for cl in range(1, lp + 1):
            print(f"\rcurrently testing for {al, bl, cl}", end="")
            a = ",".join(path_[0:al])
            b = ",".join(path_[al:al+bl])
            c = ",".join(path_[al+bl:al+bl+cl])
            compact(c)
            if skip or (len(a) <= 20 and len(b) <= 20 and len(c) <= 20):
                sol = is_completable(a, b, c, p)
                if sol:
                    return ",".join(sol), a, b, c
    return None


def mt(path_: List[str]):
    with Pool(len(path_)) as p:
        r = p.map(find_pattern_mt, ((path_, _) for _ in range(len(path_))))
    breakpoint()



def part_2(screen_: Screen):
    path = construct_path(screen)
    chars = [ord(_) for _ in ['#', '.', '^', ':', ',', ' ', '\n', '!']]

    def _out(a):
        if (a in range(ord("A"), ord("Z") + 1)
           or a in range(ord("a"), ord("z") + 1)
           or a in chars):
            print(chr(a), end="")
        else:
            print(a, end="")
    bot = IntCodeComputer(puzzle_input, output_consumer=_out)

    for line in path:
        #asciis = [ord(_) for c in line]
        for c in line:
            #if c in ['R', 'L', 'A', 'B', 'C', ',']:
            bot.input(ord(c))
            #else:
                #bot.input(int(c))
        bot.input(ord("\n"))
    bot.code[0] = 2
    bot.run()
    return None


if __name__ == '__main__':
    screen, s1 = part_1()
    print(f"Part 1: {s1}")
    s2 = part_2(screen)
    print(f"Part 2: {s2}")

