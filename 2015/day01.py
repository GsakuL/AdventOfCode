from aoc_components.puzzle_input import PuzzleInput


def up_and_down(inp):
    floor = 0
    first_basement = None
    for i, c in enumerate(inp):
        if c == ')':
            floor -= 1
        if c == '(':
            floor += 1
        if floor == -1 and (first_basement is None):
            first_basement = i+1
    return (floor, first_basement)


if __name__ == "__main__":
    a, b = up_and_down(PuzzleInput(__file__).get())
    print(f"Part 1: {a}")
    print(f"Part 2: {b}")
