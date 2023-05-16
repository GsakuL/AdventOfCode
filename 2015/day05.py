from aoc_components.input_getter import get_my_input

inp = get_my_input(__file__)


def is_nice_1(word: str):
    for x in ("ab", "cd", "pq", "xy"):
        if x in word:
            return False
    last = object()
    double = False
    vowels_count = 0
    for char in word:
        if char in "aeiou":
            vowels_count += 1
        if char == last:
            double = True
        if double and vowels_count >= 3:
            return True
        last = char
    return False


def is_nice_2(word: str):
    last2 = ""
    last3 = ""
    double = False
    group = False
    for i, char in enumerate(word):
        last2 = (last2 + char)[-2:]
        last3 = (last3 + char)[-3:]

        if i >= 1 and (not double) and word.find(last2, i+1) > 0:
            double = True
        if i >= 2 and (not group) and last3[0] == last3[2]:
            group = True
        if double and group:
            return True
    return False


if __name__ == "__main__":
    print(f"part 1: {sum(( is_nice_1(_) for _ in inp.splitlines() ))}")
    print(f"part 2: {sum(( is_nice_2(_) for _ in inp.splitlines() ))}")
