from aoc_components.input_getter import get_my_input
from aoc_components.int_code_computer import IntCodeComputer

puzzle_input = get_my_input(2019, 7)


def run_thrusters(code, *phases, write_cmd):
    last = 0
    for i in phases:
        proc_i = IntCodeComputer(code, [i, last], write_cmd=write_cmd)
        proc_i.run()
        last = proc_i.output[-1]
    return last


def run_thrusters_loop(code, *phases, write_cmd):
    current_thruster = 0
    last_value = 0
    thrusters = [
        IntCodeComputer(code, async_inputs=True, inputs=[p], name=f"{p}/{chr(65 + i)}", write_cmd=write_cmd)
        for i, p in enumerate(phases)]
    while not thrusters[4].halt:
        t = thrusters[current_thruster]
        t.run()
        t.input(last_value)
        t.run()
        last_value = t.last_()
        current_thruster += 1
        if current_thruster >= 5:
            current_thruster = 0
    return last_value


def unique(*args):
    return len(set(args)) == len(args)


def run_example(write_cmd):
    ex = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    return 43210 == run_thrusters(ex, 4, 3, 2, 1, 0, write_cmd=write_cmd)


def run_example_2(write_cmd):
    ex = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0,
          0, 5]
    res_ = run_thrusters_loop(ex, 9, 8, 7, 6, 5, write_cmd=write_cmd)
    return res_ == 139629729


def run_part_2(code, write_cmd):
    min_ = 5
    max_ = 9
    results = []
    for a in range(min_, max_+1):
        for b in range(min_, max_+1):
            for c in range(min_, max_+1):
                for d in range(min_, max_+1):
                    for e in range(min_, max_+1):
                        if not unique(a, b, c, d, e):
                            continue
                        results.append(((a, b, c, d, e),
                                        run_thrusters_loop(code, a, b, c, d, e, write_cmd=write_cmd)))
    results = sorted(results, key=lambda t: -t[1])
    if write_cmd:
        print(results[0])
    return results[0]


def run_part_1(code, write_cmd):
    results = []
    for a in range(5):
        for b in range(5):
            for c in range(5):
                for d in range(5):
                    for e in range(5):
                        if not unique(a, b, c, d, e):
                            continue
                        results.append(((a, b, c, d, e), run_thrusters(code, a, b, c, d, e, write_cmd=write_cmd)))
    results = sorted(results, key=lambda t: -t[1])
    if write_cmd:
        print(results[0])
    return results[0]


def test():
    assert run_example(False)
    assert run_example_2(False)
    assert ((1, 2, 3, 0, 4), 277328) == run_part_1(puzzle_input, False)
    assert ((6, 8, 5, 9, 7), 11304734) == run_part_2(puzzle_input, False)


if __name__ == "__main__":
    run_part_1(puzzle_input, True)
    run_part_2(puzzle_input, True)
