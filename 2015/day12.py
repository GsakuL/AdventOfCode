from aoc_components.input_getter import get_my_input
import json
from typing import Union

inp = get_my_input(__file__)


def count(ob: Union[list, dict, str, int], red=False):
    if isinstance(ob, str):
        return 0
    if isinstance(ob, int):
        return ob
    if isinstance(ob, list):
        return sum((count(o, red) for o in ob))
    if isinstance(ob, dict):
        val = list(ob.values())
        if red and "red" in val:
            return 0
        sum_ = count(list(ob.keys()), red) + count(val, red)
        return sum_
    raise RuntimeError()


if __name__ == "__main__":
    j = json.loads(inp)
    print(count(j))
    print(count(j, True))
