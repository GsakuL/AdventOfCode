from aoc_components import PuzzleInput
from typing import Any, Tuple, List, NamedTuple, Optional
import typing
from collections import Counter
import re
from dataclasses import dataclass
from hashlib import md5
ord_a = ord("a")
ord_z = ord("z")

_05 = "0" * 5
valid_pos = {str(i) for i in range(8)}


def run(puzzle: str):
    solved_1 = False
    solved_2 = 0

    pw_1: str = ""
    pw_2: List[Optional[str]] = [None] * 8

    c = 0
    while True:
        hash_ = puzzle + str(c)
        hash_hex = md5(bytes(hash_, "ascii")).hexdigest()
        if hash_hex.startswith(_05):
            if not solved_1:
                num = hash_hex[5]
                pw_1 += num
                print(f"1 found: {hash_hex[5]} with hash: {hash_}")
                if num in valid_pos and pw_2[int(num)] != -1:
                    print(f"2 found: {hash_hex[6]} with hash: {hash_}")
                    pw_2[int(num)] = hash_hex[6]
                    solved_2 += 1
        c += 1

        if (not solved_1) and len(pw_1) == 8:
            print(f"1: {pw_1}")
            solved_1 = True
        if solved_2 == 8:
            solved_2 == 100
            print("".join(pw_2))
        if (solved_1 and solved_2 > 9):
            return


if __name__ == "__main__":
    my = PuzzleInput(__file__).get()
    run(my)
