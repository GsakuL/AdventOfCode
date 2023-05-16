from typing import Dict, List, Optional, Tuple, Union

from aoc_components.int_computer import IntCodeComputer

from aoc_components.screen import Screen

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
NONE = -1


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


def turn_right(current: int):
    return {1: 4, 2: 3, 3: 1, 4: 2}[current]


def turn_left(current: int):
    return {1: 3, 2: 4, 3: 2, 4: 1}[current]


def parse_maze_with_bot():
    pos = [0, 0]

    counter = -1

    all_bots = dict()

    def get_name():
        nonlocal counter
        counter += 1
        return counter

    def _overlay():
        # return {tuple(pos): "D"}
        return {v[1]: "D" for v in all_bots.items()}

    screen = Screen(overlay=_overlay, default=" ", border=0, suppress_paint=True,
                    char_map={0: Screen.FULL_BLOCK, 1: ".", 2: "%", 9: "x"})
    remote = IntCodeComputer("day15_data.txt", async_inputs=True, write_cmd=False, name=get_name())
    last = -1
    heading = [1]

    def opposite(h):
        return {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}[h]

    _last = [1]

    def mark(heading_, pos_, val):
        screen[moved(heading_, *pos_)] = val
        screen.paint()

    def update_bot(x, y, name, remove=False):
        if remove:
            if name in all_bots:
                all_bots.pop(name)
        else:
            pos[:] = x, y
            all_bots[name] = (x, y)
        screen.paint()

    def recursive_walk(x, y, h, _last, proc: IntCodeComputer):
        if screen[moved(h, x, y)] == 2:
            pass
            # update_bot(x, y, proc.name, True)
            # return True
        if screen[moved(h, x, y)] in ("#", ".", 1, 0):
            # remote.run(opposite(h))
            # remote.last_()
            update_bot(x, y, proc.name, True)
            return False
        # update_bot(x, y, proc.name)
        # mark(HERE, (x, y), ".")
        proc.run(h)
        last_ = proc.last_()
        if last_ == 0:
            mark(h, (x, y), 0)
        else:
            mark(NONE, (x, y), last_)
            x, y, = moved(h, x, y)
            if last_ == 2:
                update_bot(x, y, proc.name, True)
                # return True
            update_bot(x, y, proc.name)
        res = (
                recursive_walk(x - 0, y, LEFT, last_, proc.copy(new_name=get_name()))
                or recursive_walk(x + 0, y, RIGHT, last_, proc.copy(new_name=get_name()))
                or recursive_walk(x, y - 0, DOWN, last_, proc.copy(new_name=get_name()))
                or recursive_walk(x, y + 0, UP, last_, proc.copy(new_name=get_name()))
        )
        update_bot(x, y, proc.name, True)
        return res

    recursive_walk(0, 0, UP, -1, remote)
    screen[(0, 0)] = 9
    # screen_.paint(True, False)
    return screen


def fill_maze(screen: Screen) -> dict:
    maze = screen.pixels.copy()
    # correct border
    for y in (screen.max_y, screen.min_y):
        for x in range(screen.min_x, screen.max_x + 1):
            maze[(x, y)] = 0
    for x in (screen.max_x, screen.min_x):
        for y in range(screen.min_y, screen.max_y + 1):
            maze[(x, y)] = 0
    # fill dead ends
    for y in range(screen.min_y, screen.max_y + 1):
        for x in range(screen.min_x, screen.max_x + 1):
            if maze._get((x, y), " ") in (" ", None):
                maze[(x, y)] = 1
    return maze


def mark_intersections(maze: dict):
    def _is_corner(dir_: List[int]):
        return (
                UP in dir_ and RIGHT in dir_
                or DOWN in dir_ and RIGHT in dir_
                or UP in dir_ and LEFT in dir_
                or DOWN in dir_ and LEFT in dir_
        )

    def _is_intersection(x, y):
        i = []
        for D in (UP, DOWN, LEFT, RIGHT):
            p = moved(D, x, y)
            if maze.get(tuple(p)) in (1, 2, 9):
                i.append(D)
        return len(i) > 2 or _is_corner(i)

    intersections = dict()
    for k, v in maze.items():
        if v in (1, 2, 9) and _is_intersection(*k):
            maze[k] = 5
            intersections[k] = set()
    return intersections


IntersectionType = Dict[Tuple[int, int], set]
MazeType = Dict[Tuple[int, int], Union[int, str]]

def map_intersections(i: IntersectionType, maze: MazeType):
    def _walk(dx, dy, x_, y_):
        while True:
            x_ += dx
            y_ += dy
            v = maze.get((x_, y_), 0)
            if v == 5:
                return x_, y_
            if v == 0:
                return None

    def _get_straight_intersections(x_, y_):
        a = [_ for _ in
             (_walk(1, 0, x_, y_), _walk(-1, 0, x_, y_), _walk(0, -1, x_, y_), _walk(0, 1, x_, y_))
             if _]
        return a

    for x, y in i.keys():
        for _ in _get_straight_intersections(x, y):
            i[x, y].add(_)


Point = Tuple[int, int]


def flatten(o: Union[list, tuple]):
    if isinstance(o, tuple):
        yield o
    else:
        for _ in o:
            yield from flatten(_)


def get_path(i: IntersectionType, start: Point, target: Point, parent: Optional[Point]):
    see = i[start] - {parent}
    if target in see:
        return start
    if not see:
        return None
    paths = list(flatten([_ for _ in (get_path(i, s, target, start) for s in see) if _]))
    if paths:
        paths.append(start)
    return paths


def calculate_length(points: List[Point]):
    def _calc(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        x = abs(x1 - x2)
        y = abs(y1 - y2)
        return y + x

    sum_ = 0
    n = len(points)
    for i in range(n-2):
        sum_ += _calc(*points[i:i+2])
    return sum_


def draw_path_on_screen(intersections: List[Point], screen_: Screen):
    for idx, inter in enumerate(intersections[:-1]):
        n = intersections[idx+1]
        dx = int(inter[0] > n[0])
        dy = int(inter[1] > n[1])
        for x in range(inter[0], n[0]+1-(2*dx), 1-(2*dx)):
            for y in range(inter[1], n[1]+1-(2 * dy), 1-(2 * dy)):
                screen_[(x, y)] = "@"


def fill_oxygen(screen: Screen, start: Point):
    path = (1, 2, 5, "@", "%", "X", ".")

    def _is_done():
        for p in path:
            if any(screen.find(p)):
                return False
        return True

    def _tiles_around(x_, y_):
        return ((moved(D, x_, y_), screen[moved(D, x_, y_)]) for D in (UP, DOWN, LEFT, RIGHT))

    minutes = 0
    screen[start] = "O"
    screen.paint(True)
    tiles_to_process = {start}
    while tiles_to_process:
        minutes += 1
        for oxygen_pos in list(tiles_to_process):
            worked = False
            for pos, tile in _tiles_around(*oxygen_pos):
                if tile in path:
                    screen[pos] = "O"
                    worked = True
                    tiles_to_process.add(pos)
            if not worked:
                if oxygen_pos in tiles_to_process:
                    tiles_to_process.remove(oxygen_pos)
        screen.paint(True)
    return minutes


def part_1():
    screen = parse_maze_with_bot()
    goal = next(screen.find(2))[0]
    maze = fill_maze(screen)
    i = mark_intersections(maze)
    i[(0, 0)] = set()
    i[goal] = set()
    maze[(0, 0)] = 5
    maze[goal] = 5
    map_intersections(i, maze)
    screen.pixels = maze


    p = get_path(i, (0, 0), goal, None)
    draw_path_on_screen(p, screen)
    screen[(0, 0)] = "X"
    screen[goal] = "%"
    ats = set(screen.find("@"))
    length = calculate_length(p)
    wrong = [(403, "too high"), (304, "too low?"), (307, "?")]
    part1 = len(ats) + 2  # 308
    screen.paint(True)

    print(f"Part 1: {part1}")

    minutes = fill_oxygen(screen, goal) # 328

    wrong = [(327, "too low")]

    breakpoint()


if __name__ == '__main__':
    part_1()
