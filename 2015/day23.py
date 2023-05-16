from aoc_components.puzzle_input import PuzzleInput


def run(code_raw: str, a=0):
    pc = 0

    r = {"a": a, "b": 0}
    code = code_raw.splitlines()
    code_l = len(code)
    while True:
        if pc >= code_l:
            break
        line = code[pc]
        op, param = line.split(" ", 1)
        if op == "hlf":
            r[param] = r[param] / 2
        elif op == "tpl":
            r[param] = r[param] * 3
        elif op == "inc":
            r[param] = r[param] + 1
        elif op == "jmp":
            pc += int(param)
            continue
        elif op == "jie":
            reg, off = param.split(", ")
            if r[reg] % 2 == 0:
                pc += int(off)
                continue
        elif op == "jio":
            reg, off = param.split(", ")
            if r[reg] == 1:
                pc += int(off)
                continue
        else:
            raise RuntimeError()
        pc += 1
    return r["b"]


if __name__ == "__main__":
    inp = PuzzleInput(__file__).get()
    print(f"Part 1: {run(inp)}")
    print(f"Part 2: {run(inp, 1)}")
