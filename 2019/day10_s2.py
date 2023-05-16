import json
import math


def main():

    def init_asteroids():
        with open("day10_data.json", "r") as fp:
            puzzle_data = json.load(fp)
        inp = puzzle_data["my_puzzle_input"]

        for y, line in enumerate(inp):
            for x, a in enumerate(line):
                if a == '#':
                    yield (x, y)

    asteroids = list(init_asteroids())

    def angle(start, end):
        result = math.atan2(end[0] - start[0], start[1] - end[1]) * 180 / math.pi
        if result < 0:
            return 360 + result
        return result

    # part 1
    result = None
    m = 0

    for start in asteroids:
        cnt = len({angle(start, end) for end in asteroids if start != end})
        if cnt > m:
            m = cnt
            result = start

    print('x {} y {}'.format(*result))
    print('visible {}'.format(m))

    # part 2
    asteroids.remove(result)
    angles = sorted(
        ((angle(result, end), end) for end in asteroids),
        key=lambda x: (x[0], abs(result[0] - x[1][0]) + abs(result[1] - x[1][1]))
    )

    idx = 0
    last = angles.pop(idx)
    last_angle = last[0]
    cnt = 1

    while cnt < 200 and angles:
        if idx >= len(angles):
            idx = 0
            last_angle = None
        if last_angle == angles[idx][0]:
            idx += 1
            continue
        last = angles.pop(idx)
        last_angle = last[0]
        cnt += 1
    print('vaporized {}: {} {}'.format(cnt, last[1], last[1][0] * 100 + last[1][1]))


if __name__ == '__main__':
    main()
