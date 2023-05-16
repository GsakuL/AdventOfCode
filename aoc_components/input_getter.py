import os
import re
from os import path
from os.path import isfile, isdir
import re
import requests
from typing import List, TypeVar, Type, overload

T = TypeVar('T')

cookie_path = path.join("aoc_components", "_session_cookie.txt")

if not isfile(cookie_path):
    raise FileNotFoundError(f"please supply your session cookie in {path.abspath(cookie_path)}")
with open(cookie_path, "r") as fp:
    sc = fp.read().strip()

cookies = {"session": sc}


def _get_date_code(file: str):
    year = os.path.split(os.path.dirname(file))[-1]
    m = re.match(r"[a-zA-Z_-]*(\d+)\.py", os.path.basename(file))
    if not m:
        raise RuntimeError()
    day = m[1]
    return int(year), int(day)


@overload
def get_my_input(a: int, b: int) -> str:
    pass


@overload
def get_my_input(a: str) -> str:
    pass


def get_my_input(a, b=None) -> str:
    if isinstance(a, str) and not b:
        year, day = _get_date_code(a)
    else:
        year, day = a, b
        if day > year:
            year, day = day, year
    input_path = path.join(str(year), "input")
    if not isdir(input_path):
        os.mkdir(input_path)
    file_name = path.join(input_path, f"{year}_{day:02d}.txt")
    if isfile(file_name):
        with open(file_name, "r") as fp_:
            return fp_.read().strip()
    url = f"https://adventofcode.com/{year}/day/{day}/input"

    r = requests. get(url, cookies=cookies)
    r.encoding = "utf8"
    if r.status_code != requests.codes.ok:
        raise requests.ConnectionError(f"cannot get '{url}'. Error: {r.status_code} {r.text}")
    text = r.text.strip()
    with open(file_name, "w") as fp_:
        fp_.write(text)
    return text


def get_my_list(year: int, day: int, *, t: Type[T] = str, d=r"[\n\r]+|,|;") -> List[T]:
    inp = get_my_input(year, day)
    return [t(_) for _ in re.split(d, inp)]

def get_my_int_list(year: int, day: int, delimiter_re=r"[\n\r]+|,|;") -> List[int]:
    inp = get_my_input(year, day)
    return [int(_) for _ in re.split(delimiter_re, inp)]

