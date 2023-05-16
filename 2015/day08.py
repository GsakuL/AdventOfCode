from aoc_components.input_getter import get_my_input

inp = get_my_input(__file__)


def eval_len(text: str):
    count = 0
    text = text[1:-1]
    mx = len(text)
    i = 0
    while i < mx:
        char = text[i]
        if char != "\\":
            count += 1
            i += 1
            continue
        nx = text[i+1]
        if nx in ('"', "\\"):
            count += 1
            i += 2
        elif nx == 'x':
            count += 1
            i += 4
    return count


def escape(text: str):
    count = 2
    mx = len(text)
    i = 0
    while i < mx:
        char = text[i]
        if char in ('"', "\\"):
            count += 1
        count += 1
        i += 1
    return count


if __name__ == "__main__":
    nums = []
    for line in inp.splitlines():
        nums.append((len(line), eval_len(line), escape(line)))
    print(f"Part 1: {sum((L-v for L,v,e in nums))}")
    print(f"Part 2: {sum((e-L for L,v,e in nums))}")
