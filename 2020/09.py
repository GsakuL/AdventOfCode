from collections import deque
import re
from typing import Dict, List, NamedTuple, Optional, Set, TypedDict

from aoc_components import PuzzleInput

example_data_1 = """
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""


class Runner:

    def __init__(self, data: List[int], length: int) -> None:
        self.data = data
        self.size = len(self.data)
        self.last = deque(data[0:length], length)
        self.index = length

    @staticmethod
    def parse(data: str, length: int):
        numbers = [int(n) for n in data.splitlines() if n]
        return Runner(numbers, length)

    def is_summable(self, target: int) -> bool:
        for i, v in enumerate(self.last):
            for j, w in enumerate(self.last):
                if i == j or v == w:
                    continue
                if v + w == target:
                    return True
        return False

    def step(self) -> bool:
        target = self.data[self.index]
        summable = self.is_summable(target)
        self.last.append(target)
        self.index += 1
        return summable

    def till_end(self):
        done = False
        while not done:
            done = not self.step()
        return self.data[self.index - 1]

    def find_strip(self, target: int):
        for start in range(self.size):
            for end in range(self.size):
                if start >= end:
                    continue
                _range = self.data[start:(end + 1)]
                if sum(_range) == target:
                    return min(_range) + max(_range)


if __name__ == "__main__":
    ex1 = Runner.parse(example_data_1, 5)

    assert ex1.till_end() == 127
    assert ex1.find_strip(127) == 62

    puzzle = PuzzleInput(__file__)()

    runner = Runner.parse(puzzle, 25)
    result_1 = runner.till_end()
    print(f"{result_1=}")

    result_2 = runner.find_strip(result_1)
    print(f"{result_2=}")
