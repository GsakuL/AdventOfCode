from aoc_components.input_getter import get_my_input
import hashlib

inp = get_my_input(__file__)


num = 1
o5 = "0"*5
day1 = False
day2 = False
while True:
    h = hashlib.md5(bytes(f"{inp}{num}", "utf8")).hexdigest()
    if h.startswith(o5):
        if h[5] == "0":
            if not day2:
                print(f"day 2: {num}")
            day2 = True
        else:
            if not day1:
                print(f"day 1: {num}")
            day1 = True
    if day1 and day2:
        break
    num += 1
