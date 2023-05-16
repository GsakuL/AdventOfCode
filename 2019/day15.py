import sys
from typing import Any, Collection, Dict, NamedTuple, Tuple, Union

from colorama import Fore, Style

from aoc_components.input_getter import get_my_input
from aoc_components.int_code_computer import IntCodeComputer
from aoc_components.screen import Screen

puzzle_input = get_my_input(2019, 15)

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

WALL = 0
EMPTY_SPACE = 1
OXYGEN_MODULE = 2
START = 3
OXYGEN = 4
PATH = 5

important_pixels = {(0, 0): START}


def moved(h, x, y):
    if h == UP:
        y += 1
    elif h == DOWN:
        y -= 1
    elif h == LEFT:
        x -= 1
    elif h == RIGHT:
        x += 1
    return x, y


class MazeReturn(NamedTuple):
    exit: Any
    path: Any

    def __bool__(self):
        return bool(self.exit)


def parse_maze_with_bot(animate: bool, code):
    screen = Screen(overlay=lambda: important_pixels, default=" ", border=1, suppress_paint=not animate,
                    char_map={
                        WALL: Screen.FULL_BLOCK,
                        EMPTY_SPACE: f"{Fore.YELLOW}{Screen.FULL_BLOCK}{Fore.RESET}",
                        OXYGEN_MODULE: f"{Fore.MAGENTA}{Screen.FULL_BLOCK}{Fore.RESET}",
                        START: f"{Fore.GREEN}{Style.DIM}{Screen.FULL_BLOCK}{Fore.RESET}",
                        OXYGEN: f"{Fore.BLUE}{Screen.FULL_BLOCK}{Fore.RESET}",
                        PATH: f"{Fore.CYAN}{Screen.FULL_BLOCK}{Fore.RESET}",
                    })
    remote = IntCodeComputer(code, async_inputs=True, write_cmd=False)

    def mark(pos_, val):
        screen[tuple(pos_)] = val
        if animate:
            screen.paint()

    best_path = set()

    def recursive_walk(x, y, h, proc: IntCodeComputer):
        if screen[moved(h, x, y)] in (EMPTY_SPACE, WALL):
            return False, False

        proc.run(h)
        last_ = proc.last_()
        if last_ == 0:
            mark(moved(h, x, y), 0)
        else:
            mark((x, y), 1,)
            x, y, = moved(h, x, y)
            mark((x, y), last_)
        found = False
        for d in (LEFT, RIGHT, DOWN, UP):
            res, is_path = recursive_walk(x, y, d, proc.copy())
            found |= is_path
            if res:
                break
        if found:
            best_path.add((x, y))
        return res, (found or screen[(x, y)] == 2)

    recursive_walk(0, 0, UP, remote)
    best_path.remove((0, 0))
    screen[(0, 0)] = START
    screen.paint()

    return screen, best_path


def fill_maze(screen: Screen):
    def _tiles_around(x_, y_):
        return ((moved(D, x_, y_), screen[moved(D, x_, y_)]) for D in (UP, DOWN, LEFT, RIGHT))

    # correct border
    for y in (screen.max_y, screen.min_y):
        for x in range(screen.min_x, screen.max_x + 1):
            screen[(x, y)] = 0
    for x in (screen.max_x, screen.min_x):
        for y in range(screen.min_y, screen.max_y + 1):
            screen[(x, y)] = 0
    # fill dead ends
    for y in range(screen.min_y, screen.max_y + 1):
        for x in range(screen.min_x, screen.max_x + 1):
            if screen[(x, y)] in (" ", None):
                is_walled_in = all((t[1] == 0 for t in _tiles_around(x, y)))
                screen[(x, y)] = int(not is_walled_in)


IntersectionType = Dict[Tuple[int, int], set]
MazeType = Dict[Tuple[int, int], Union[int, str]]

Point = Tuple[int, int]


def draw_path_on_screen(intersections: Collection[Point], screen_: Screen):
    for inter in intersections:
        screen_[inter] = PATH


def fill_oxygen(screen: Screen, start: Point, paint: bool = True):
    path = (EMPTY_SPACE, OXYGEN_MODULE, START, PATH)

    def _tiles_around(x_, y_):
        return ((moved(D, x_, y_), screen[moved(D, x_, y_)]) for D in (UP, DOWN, LEFT, RIGHT))

    minutes = 0
    screen[start] = OXYGEN
    tiles_to_process = {start}
    while tiles_to_process:
        for oxygen_pos in list(tiles_to_process):
            worked = False
            for pos, tile in _tiles_around(*oxygen_pos):
                if tile in path:
                    screen[pos] = OXYGEN
                    worked = True
                    tiles_to_process.add(pos)
            if not worked:
                if oxygen_pos in tiles_to_process:
                    tiles_to_process.remove(oxygen_pos)
        if tiles_to_process:
            minutes += 1
        if paint:
            screen.paint()
    return minutes


def part_1(animate, code):
    screen, best_path = parse_maze_with_bot(animate, code)
    goal = next(screen.find(OXYGEN_MODULE))[0]
    important_pixels[goal] = OXYGEN_MODULE
    fill_maze(screen)
    screen[(0, 0)] = START
    screen[goal] = OXYGEN_MODULE
    if animate:
        screen.paint()

    wrong = [(403, "too high"), (304, "too low?"), (307, "?")]

    minutes = fill_oxygen(screen, goal, False)  # 328
    draw_path_on_screen(best_path, screen)
    screen.suppress_paint = False
    screen.paint()
    print(f"Part 1: {len(best_path)}")
    wrong = [(327, "too low")]
    print(f"Part 2: {minutes}")
    # breakpoint()


if __name__ == '__main__':
    arg = sys.argv[1:]
    part_1("animate" in arg, puzzle_input)
