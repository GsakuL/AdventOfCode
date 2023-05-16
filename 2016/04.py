from aoc_components import PuzzleInput
from typing import Any, Tuple, List, NamedTuple, Optional
import typing
from collections import Counter
import re
from dataclasses import dataclass

ord_a = ord("a")
ord_z = ord("z")


@dataclass
class Room:
    names: List[str]
    counter: typing.Counter[str]
    sector: int
    checksum: str
    _decrypted: Optional[List[str]] = None

    @staticmethod
    def parse(raw: str):
        name_id, checksum = raw.lower().strip().split("[")
        checksum = checksum.strip("]")
        name_id_parts = name_id.split("-")
        name = "".join(name_id_parts[:-1])
        return Room(name_id_parts[:-1], Counter(name), int(name_id_parts[-1]), checksum)

    @property
    def is_valid(self):
        sort = sorted(self.counter.items(), key=lambda c: (-c[1], c[0]))[0:5]
        return "".join((s[0] for s in sort)) == self.checksum

    def _decrypt_char(self, char: str):
        global ord_a
        o = (ord(char) + self.sector - ord_a) % 26 + ord_a
        return chr(o)

    def _decrypt_name(self, name: str):
        return "".join((self._decrypt_char(c) for c in name))

    @property
    def decrypted(self):
        if self._decrypted is None:
            self._decrypted = [self._decrypt_name(n) for n in self.names]
        return self._decrypted


def parse(puzzle: str):
    return [Room.parse(line) for line in puzzle.strip().split("\n")]


def run(puzzle: str):
    rooms = parse(puzzle)
    sector_sum = 0
    match = ['northpole', 'object', 'storage']
    matched = False
    for r in rooms:
        if not r.is_valid:
            continue
        sector_sum += r.sector
        if (not matched) and r.decrypted == match:
            print(f"{match}: {r.sector}")
            matched = True
    print(f"{sector_sum=}")


if __name__ == "__main__":
    my = PuzzleInput(__file__).get()
    run(my)
