from aoc_components.input_getter import get_my_input
inp = get_my_input(__file__)


def is_valid(pw: str) -> bool:
    for x in "iol":
        if x in pw:
            return False
    vals = [ord(_) for _ in pw]
    inc = False
    last_double = -1
    doubles = 0
    for _ in range(8):
        try:
            a, b, c = vals[_:_+3]
            if a+1 == b and a+2 == c:
                inc = True
        except (ValueError, IndexError):
            pass

        try:
            if doubles < 2 and last_double < _ and vals[_] == vals[_+1]:
                doubles += 1
                last_double = _+1
        except IndexError:
            pass
        if inc and doubles >= 2:
            return True
    return False


def inc_(pw: str, index: int):
    char = pw[index]
    char = ord(char)+1
    overflow = False
    if char > ord("z"):
        overflow = True
        char = ord("a")
    _pw = list(pw)
    _pw[index] = chr(char)
    pw = "".join(_pw)
    if overflow:
        return inc_(pw, index-1)
    return pw


def inc(pw: str):
    i = 7
    while True:
        pw = inc_(pw, i)
        if is_valid(pw):
            return pw


if __name__ == "__main__":
    assert inc("abcdefgh") == "abcdffaa"
    pw = inc(inp)
    print(f"Part 1: {pw}")
    pw = inc(pw)
    print(f"Part 2: {pw}")
