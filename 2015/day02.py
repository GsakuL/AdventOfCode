from aoc_components.puzzle_input import PuzzleInput


def wrap(inp):
    paper = 0
    ribbon = 0
    for p in inp.splitlines():
        x, y, z = map(int, p.split("x"))
        a = x * y
        b = y * z
        c = x * z
        m = min(a, b, c)
        paper += ((2 * (a + b + c)) + m)
        wrap = sum(sorted([x, y, z])[0:2]) * 2
        ribbon += (wrap + (x * y * z))
    return paper, ribbon


if __name__ == "__main__":
    paper, ribbon = wrap(PuzzleInput(__file__).get())
    print(f"part 1: {paper}")
    print(f"part 2: {ribbon}")
