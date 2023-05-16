from aoc_components.input_getter import get_my_input
from aoc_components.int_code_computer import IntCodeComputer

puzzle_input = get_my_input(2019, 5)

demo_jump_pos = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
demo_jump_imm = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]

demo_compare_8 = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                  1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                  999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]


def _run(i):
    proc = IntCodeComputer(puzzle_input, [i], write_cmd=False)
    proc.run()
    return proc.last_()


if __name__ == "__main__":
    print(f"Part 1: {_run(1)}\nPart 2:{_run(5)}")
