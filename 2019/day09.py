from aoc_components.input_getter import get_my_input
from aoc_components.int_code_computer import IntCodeComputer

puzzle_input = get_my_input(2019, 9)


def test():
    run_examples()
    run_part_1()
    run_part_2()


def run_examples():
    code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    proc = IntCodeComputer(code, write_cmd=False)
    proc.run()
    result = list(proc.output)
    assert result == code

    code = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    proc = IntCodeComputer(code, write_cmd=False)
    proc.run()
    assert 1219070632396864 == proc.last_()

    code = [104, 1125899906842624, 99]
    proc = IntCodeComputer(code, write_cmd=False)
    proc.run()
    assert 1125899906842624 == proc.last_()


def run_part_1():
    proc = IntCodeComputer(puzzle_input, [1], write_cmd=False)
    proc.run()
    assert 4080871669 == proc.last_()


def run_part_2():
    proc = IntCodeComputer(puzzle_input, [2], write_cmd=False)
    proc.run()
    print(list(proc.output))
    assert 75202 == proc.last_()


if __name__ == "__main__":
    asyncio.run(run_part_2())
