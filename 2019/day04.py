import re

from aoc_components.input_getter import get_my_int_list

range_min, range_max = get_my_int_list(2019, 4, "-")


def has_duplicate_number(pw):
    return any((_ in pw for _ in (str(r)*2 for r in range(10))))


def only_increases(pw):
    last = int(pw[0])
    for c in pw[1:]:
        new = int(c)
        if new < last:
            return False
        last = new
    return True


def is_valid(pw):
    return has_duplicate_number(pw) and only_increases(pw)


def has_exact_double_number(pw):
    for d in range(10):
        m = re.findall(rf"{d}+", pw)
        if m and all((len(_) == 2 for _ in m)):
            return True
    return False


def has_only_double_duplicate_number(pw):
    for d in range(10):
        m = re.findall(rf"{d}{d}+", pw)
        if m and any((_ for _ in m if len(_) > 2)):
            return has_exact_double_number(pw)
    return True


def is_valid_2(pw):
    return is_valid(pw) and has_only_double_duplicate_number(pw)


def part_1():
    valid_pw = sum(int(is_valid(str(n))) for n in range(range_min, range_max+1))
    print(valid_pw)


def test_2():
    print(is_valid_2('112233'))
    print(not is_valid_2('123444'))
    print(is_valid_2('111122'))


def part_2():
    valid_pw = sum(int(is_valid_2(str(n))) for n in range(range_min, range_max + 1))
    print(valid_pw)

part_2()
wrong_2 = [590, "too low"]

