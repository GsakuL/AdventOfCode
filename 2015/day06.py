from aoc_components.input_getter import get_my_input
from collections import defaultdict
import re
inp = get_my_input(__file__)

grid = defaultdict(bool)
grid2 = defaultdict(int)
r = re.compile(r"(toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)")

for l in inp.splitlines():
    m = r.match(l)
    if not m:
        raise RuntimeError()
    mode = m[1]
    a = int(m[2])
    b = int(m[3])

    f = int(m[4])
    g = int(m[5])
    for x in range(a, f+1):
        for y in range(b, g+1):
            if mode == "toggle":
                new = not grid[(x, y)]
                new2 = 2
            elif mode == "turn on":
                new = True
                new2 = 1
            elif mode == "turn off":
                new = False
                new2 = -1
            else:
                raise RuntimeError()
            new2 += grid2[(x, y)]
            if new2 < 0:
                new2 = 0
            grid2[(x, y)] = new2
            grid[(x, y)] = new


if __name__ == "__main__":
    print(f"part 1: {sum(grid.values())}")
    print(f"part 2: {sum(grid2.values())}")
