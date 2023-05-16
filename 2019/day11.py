from typing import List

from aoc_components.input_getter import get_my_input
from aoc_components.int_code_computer import IntCodeComputer
from aoc_components.screen import Screen

puzzle_input = get_my_input(2019, 11)


def rotate(rot: int, i: int):
    i += (rot * 2) - 1
    if i > 3:
        i = 0
    elif i < 0:
        i = 3
    return i


def move(pos: List[int]):
    x, y, d = pos
    if d == 0:
        y += 1
    elif d == 1:
        x += 1
    elif d == 2:
        y -= 1
    elif d == 3:
        x -= 1
    else:
        raise ValueError(f"unknown rotation value: {d}")
    pos[:] = x, y, d


def part_1(start_value):
    pos = [0, 0, 0]
    is_color = [True]
    screen_ = Screen(default=0, char_map={0: " ", 1: Screen.FULL_BLOCK}, pixels={(0, 0): start_value})

    def _out(i):
        if is_color[0]:
            screen_[pos[:2]] = i
        else:
            pos[2] = rotate(i, pos[2])
        is_color[0] ^= True

    bot = IntCodeComputer(puzzle_input, async_inputs=True, write_cmd=False, output_consumer=_out)
    while not bot.halt:
        bot.run()
        current_color = screen_[pos[:2]]
        bot.input(current_color)
        bot.run()
        move(pos)
    return screen_


if __name__ == '__main__':
    screen = part_1(0)

    print("Part 1=" + str(len(screen.pixels)))
    print("Part 2:")
    screen = part_1(1)
    screen.paint()
