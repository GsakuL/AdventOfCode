from collections import defaultdict
from aoc_components.input_getter import get_my_input

inp = get_my_input(__file__)


paper = []

visited = defaultdict(int)

x = 0
y = 0

pos_g = [[0, 0], [0, 0]]
pos_i = 0


def netx_pos():
    global pos_i
    global pos_g
    r = pos_g[pos_i]
    pos_i = abs(pos_i - 1)
    return r


visited[(x, y)] = 1

for d in inp:
    pos = netx_pos()
    x, y = pos
    if d == "<":
        x -= 1
    elif d == ">":
        x += 1
    elif d == "v":
        y -= 1
    elif d == "^":
        y += 1
    pos[:] = (x, y)
    visited[tuple(pos)] = visited[tuple(pos)] + 1


print(f"part 2: {len([v for k,v in visited.items() if v >= 1])}")


# too high: 30672640756
