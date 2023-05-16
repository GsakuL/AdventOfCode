import re
from typing import Dict, List, NamedTuple, Optional, Set, TypedDict

from aoc_components import PuzzleInput

tests = [
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
]

def find(data: str, window_size = 4):
    c = 0
    while True:
        window = set(data[c:c+window_size])
        if len(window) == window_size:
            return c + window_size # account for minim frame size
        c += 1

def run_test():
    for text, count in tests:
        found = find(text)
        if found != count:
            raise ValueError(f"found {found}. Expected {count}")

if __name__ == "__main__":
    run_test()
    puzzle = PuzzleInput(__file__).get()

    print(f"Part 1: {find(puzzle)}")
    print(f"Part 2: {find(puzzle, 14)}")