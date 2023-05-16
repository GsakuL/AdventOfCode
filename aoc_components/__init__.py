from .int_code_computer import IntCodeComputer
from .puzzle_input import PuzzleInput
from .screen import Screen, Transform

__all__ = [
    "PuzzleInput",
    "Screen",
    "Transform",
    "IntCodeComputer",
    "remove_all",
]


def remove_all(txt: str, *sub: list[str]):
    for s in sub:
        txt = txt.replace(s, "")
    return txt
