from aoc_components.input_getter import get_my_input
inp = get_my_input(__file__)


def say_(number: str):
    last = number[0]
    c = 1
    for n in number[1:]:
        if last == n:
            c += 1
        else:
            yield str(c)
            yield last
            c = 1
        last = n
    yield str(c)
    yield last


def say(number: str):
    return "".join(say_(number))


if __name__ == "__main__":
    num = inp
    for _ in range(40):
        num = say(num)
    print(len(num))

    for _ in range(10):
        num = say(num)
    print(len(num))
