
from typing import List

import numpy as np
from colorama import Fore

from aoc_components.input_getter import get_my_input

pattern = [0, 1, 0, -1]
pre_built_patterns = {}


def build_pattern(iteration: int, length: int):
    global pattern
    pattern_ = np.tile(pattern, 1+int(np.ceil(length / len(pattern))))

    p = pre_built_patterns.get(iteration, None)
    if p is None:
        p = np.delete(np.delete(np.repeat(pattern_, iteration), 0), slice(length, None))
        pre_built_patterns[iteration] = p
    return p



num = np.array([])

ln = len(num)

def import_data(file="day16_data.txt", number="", multi=1):
    global num
    global ln
    if number:
        r = number
    else:
        with open(file) as fp:
            r = fp.read()
    i = [int(_) for _ in r*multi]
    num = np.array(i)
    ln = len(num)





def ones(a):
    a = abs(a)
    return int(((a / 10) - (a // 10)) * 10)


seen = set()


def phase(arr: np.ndarray, i: int):
    global ln
    arr = np.array([
        np.sum(np.multiply(arr, build_pattern(r+1, ln)))
        for r in range(ln)
    ])

    abs_ = np.abs(arr)
    subs = np.floor_divide(abs_, 10)
    diffs = np.multiply(subs, 10)
    result = np.subtract(abs_, diffs)
    return result


def arr_to_int(a):
    return "".join((str(_) for _ in a))

def find_repeat(arr: List[str], pos: int):
    found = False
    search = pattern_ = "".join(s[pos] for s in arr)[:-1]
    pattern_len = 1

    while pattern_len <= len(search):
        p_ = pattern_[0:pattern_len]
        if search.startswith(p_*2):
            print(f"For pos {pos}, repeat {pattern_len}")
            return
        pattern_len += 1
    print(f"found no repeat for pos {pos}")


offset = 5971989
base_len = 650

if __name__ == '__main__':
    i = get_my_input(2019, 16)
    ps = list()
    for _ in range(1_000):
        ps.append(build_pattern(_+1, base_len * 10_000)[offset-1:offset + 8])
    runs = []
    #import_data(multi=10_000)
    import_data(number="80871224585914546619083218645595")
    #import_data(number="12345678")

    for _ in range(1_000):
        print(f"\r{_}", end="")

        # seen.add(arr_to_int(num))
        num = phase(num, _+1)
        n = arr_to_int(num)
        runs.append(n)
        # if arr_to_int(num) in seen:
         #   print(f"repeat at {_}")
    print()
    for _ in runs:
        print(str(_)
              .replace("3", "#3#",)
              .replace("4", "#4#",)
              .replace("5", "#5#",)
              .replace("6", "#6#",)
              .replace("7", "#7#",)

              .replace("#3#", f"{Fore.MAGENTA}3{Fore.RESET}")
              .replace("#4#", f"{Fore.YELLOW}4{Fore.RESET}")
              .replace("#5#", f"{Fore.CYAN}5{Fore.RESET}")
              .replace("#6#", f"{Fore.BLUE}6{Fore.RESET}")
              .replace("#7#", f"{Fore.GREEN}7{Fore.RESET}")
              )
    for _ in range(ln):
        find_repeat(runs, _)
    first = np.delete(num, slice(8, None))
    #print(f"Part 1: {32002835}")
