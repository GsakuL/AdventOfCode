from collections import Counter
from typing import List

from aoc_components.input_getter import get_my_input
from aoc_components.screen import Screen, Transform

puzzle_height = 6
puzzle_width = 25

puzzle_input = get_my_input(2019, 8)


def parse_image_to_layers(image: str, width, height):
    rows = [image[i:i + width] for i in range(0, len(image), width)]
    layers = []
    while rows:
        layers.append([rows.pop(0) for _ in range(height)])
    return layers


def run_part_1():
    layers = parse_image_to_layers(puzzle_input, puzzle_width, puzzle_height)
    res = find_layer(layers, "0", min)
    c = Counter("".join(res))
    print(c["1"] * c["2"])


def run_part_2():
    layers = parse_image_to_layers(puzzle_input, puzzle_width, puzzle_height)
    screen = combine_layers(layers, puzzle_width, puzzle_height)
    screen.paint()


def get_first_visible_pixel(layers, w, h):
    for L in range(len(layers)):
        p = layers[L][h][w]
        if p != "2":
            return p
    return "9"


def combine_layers(layers: List[List[str]], width, height):
    s = Screen(default=0, char_map={'0': " ", '1': Screen.FULL_BLOCK}, transform=Transform.ORIGIN_TOP_LEFT)
    for w in range(width):
        for h in range(height):
            p = get_first_visible_pixel(layers, w, h)
            s[w, h] = p
    return s


def find_layer(layers: List[List[str]], value, func):
    res = [sum((r.count(str(value)) for r in L)) for L in layers]
    return layers[res.index(func(res))]


if __name__ == "__main__":
    run_part_2()
