from aoc_components.input_getter import get_my_input
from typing import List
from dataclasses import dataclass
import re
inp = get_my_input(__file__)


@dataclass
class Deer:
    name: str
    speed: int  # km/s
    duration: int  # s
    resting: int  # s
    current_resting: bool = False
    current_timer = 0
    current_distance: int = 0
    points: int = 0

    def travel(self, seconds: int):
        dist = 0
        while seconds > 0:
            s = min(self.duration, seconds)
            dist += (self.speed * s)
            seconds -= (s + self.resting)
        return dist

    def travel_single(self):
        if self.current_resting:
            if self.current_timer == self.resting:
                self.current_resting = False
                self.current_timer = 1
                self.current_distance += self.speed
            else:
                self.current_timer += 1
        else:
            if self.current_timer == self.duration:
                self.current_resting = True
                self.current_timer = 1
            else:
                self.current_timer += 1
                self.current_distance += self.speed


r = re.compile(r"^([a-zA-Z]+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$")


def parse(line: str) -> Deer:
    global r
    m = r.match(line)
    if not m:
        raise RuntimeError()
    return Deer(m[1], int(m[2]), int(m[3]), int(m[4]))


def main():
    deers: List[Deer] = []

    for line in inp.splitlines():
        deers.append(parse(line))

    print(max(
        (d.travel(2503) for d in deers)
    ))

    m = 0
    for _ in range(2503):
        for d in deers:
            d.travel_single()
            m = max(m, d.current_distance)
        for d in deers:
            if d.current_distance == m:
                d.points += 1

    print(max((d.points for d in deers)))


if __name__ == "__main__":
    main()
