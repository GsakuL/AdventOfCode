from typing import List

from aoc_components.input_getter import get_my_list

puzzle_input = get_my_list(2019, 2, t=int)

example_1 = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]

solution_1 = [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]


def add_(code: List[int], index: int):
    work(code, index, lambda a, b: a + b)


def multiply_(code: List[int], index: int):
    work(code, index, lambda a, b: a * b)


def work(code: List[int], index: int, func):
    a = code[code[index + 1]]
    b = code[code[index + 2]]
    code[code[index + 3]] = func(a, b)


def process_code(code: List[int]):
    index = 0
    while True:
        op_code = code[index]
        if op_code == 1:
            add_(code, index)
        elif op_code == 2:
            multiply_(code, index)
        elif op_code == 99:
            break
        else:
            print(f"ERROR: OP Code '{op_code}' unknown", code)
        index += 4
    # print("done:", code)
    return code


part1 = puzzle_input.copy()
part1[1] = 12
part1[2] = 2

process_code(part1)
print("done:", part1)

for noun in range(100):
    for verb in range(100):
        mem = puzzle_input.copy()
        mem[1] = noun
        mem[2] = verb
        try:
            process_code(mem)
            if 19690720 == mem[0]:
                print(f"noun: {noun}. verb: {verb}. answer: {100 * noun + verb}")
        except Exception as e:
            print(e)
