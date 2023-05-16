from aoc_components import PuzzleInput

from typing import NamedTuple, TypedDict, Optional
import re


def num(r: str, mi: int, ma: int):
    return r and r.isnumeric() and (mi <= int(r) <= ma)


def year(r: str, mi: int, ma: int):
    return (r and len(r) == 4 and num(r, mi, ma))


def byr(r: str):
    return year(r, 1920, 2002)


def iyr(r: str):
    return year(r, 2010, 2020)


def eyr(r: str):
    return year(r, 2020, 2030)


def hgt(r: str):
    if r:
        unit = r[-2:]
        ammount = r[:-2]
        if unit == "cm":
            return num(ammount, 150, 193)
        elif unit == "in":
            return num(ammount, 59, 76)
    return False


hcl_re = re.compile(r"#[0-9a-f]{6}", re.IGNORECASE)


def hcl(r: str):
    return r and hcl_re.match(r)


ecl_values = "amb blu brn gry grn hzl oth".split(" ")


def ecl(r: str):
    return r and (r in ecl_values)


def pid(r: str):
    #return r and (1 <= len(r) <= 9) and r.isnumeric()
    return r and len(r) == 9 and r.isnumeric()

needed = {
    "byr": byr,
    "iyr": iyr,
    "eyr": eyr,
    "hgt": hgt,
    "hcl": hcl,
    "ecl": ecl,
    "pid": pid,
    # "cid": cid
}



def is_valid2(p: dict):
    for k, v in p.items():
        if k == "cid":
            continue
        if v is None:
            return False
    return True


def is_valid(p: dict):
    required = valid = True
    for k, v in needed.items():
        item = p.get(k)
        if item is None:
            required = False
            valid = False
            break
        else:
            valid &= bool(v(item))

    return (required, valid)


def create(line: str):
    pairs = [p.split(":") for p in line.strip().split(" ")]
    d = {k: v for k, v in pairs}
    return d


def parse(raw_data: str):
    current = ""
    passports = []
    for line in raw_data.splitlines():
        if not line.strip():
            passports.append(create(current))
            current = ""
        else:
            current += " " + line

    if current.strip():
        passports.append(create(current))
    return passports


if __name__ == "__main__":
    puzzle = PuzzleInput(__file__).get()
    passports = parse(puzzle)
    result = [(is_valid(p), p) for p in passports]

    valid = [r[1] for r in result if r[0][1]]
    for i in range(2):
        print(sum((_[0][i] for _ in result)))
    print()
