from aoc_components import PuzzleInput
from typing import List, NamedTuple


class PasswordWithPolicy(NamedTuple):
    min_: int
    max_: int
    letter: str
    passwd: str
    valid_old: bool
    valid_new: bool

def parse_line(line: str):
    policy, passwd  =line.split(":")
    range_, letter = policy.split(" ")
    min_, max_ = range_.split("-")
    min_, max_ = int(min_), int(max_)
    passwd = passwd.strip()
    valid_old = passwd.count(letter) in range(min_, max_ + 1)
    a = passwd[min_-1] == letter
    b = passwd[max_-1] == letter
    valid_new = a ^ b
    return PasswordWithPolicy(min_, max_, letter, passwd, valid_old, valid_new)

if __name__ == "__main__":
    pws = PuzzleInput(__file__).as_list("\n", parse_line)
    print(sum((p.valid_old for p in pws)))
    print(sum((p.valid_new for p in pws)))
