from aoc_components.input_getter import get_my_input
from aoc_components.int_code_computer import IntCodeComputer
from aoc_components.screen import Screen, Transform

puzzle_input = get_my_input(2019, 13)


def part_1():
    parts = []
    screen = Screen(transform=Transform.ORIGIN_TOP_LEFT,
                    char_map={0: " ", 1: Screen.FULL_BLOCK, 2: "#", 3: "-", 4: "o"}, )
    score = 0

    def _out(i: int):
        parts.append(i)

        if len(parts) == 3:
            x, y, o = parts
            screen[x, y] = o
            parts.clear()

    arcade = IntCodeComputer(puzzle_input, async_inputs=True, output_consumer=_out, )

    arcade.run()
    blocks = len(list(screen.find(2)))
    print(f"Part 1:{blocks}")


def part_2():
    parts = []
    screen = Screen(transform=Transform.ORIGIN_TOP_LEFT,
                    char_map={0: " ", 1: Screen.FULL_BLOCK, 2: "#", 3: "-", 4: "o"}, )
    score = [0]

    def _out(i: int):
        parts.append(i)

        if len(parts) == 3:
            x, y, o = parts
            if (x, y) == (-1, 0):
                score[0] = o
                parts.clear()
            else:
                screen[x, y] = o
                parts.clear()

    arcade = IntCodeComputer(puzzle_input, async_inputs=True, output_consumer=_out, )
    arcade.code[0] = 2
    blocks = float('inf')
    ball = (0, 0)
    paddle = (0, 0)
    while not (arcade.halt or blocks == 0):
        arcade.run()

        blocks = len(list(screen.find(2)))
        ball = next(screen.find(4))[0]
        paddle = next(screen.find(3))[0]
        new = ball[0] - paddle[0]
        if new != 0:
            new = new // abs(new)
        arcade.input(new)
    print(f"Part 2:{score[0]}")


if __name__ == '__main__':
    part_1()
    part_2()

