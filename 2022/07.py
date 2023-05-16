from dataclasses import dataclass, field
import re
from typing import Dict, Generator, List, NamedTuple, Optional, Protocol, Set, TypedDict

from aoc_components import PuzzleInput

class Sizable(Protocol):
    size: int

@dataclass
class File:
    name: str
    size: int

@dataclass
class Dir:
    name: str
    parent: Optional['Dir'] = None
    content: list['Sizable'] = field(default_factory=list)
    _size: int | None = None

    @property
    def size(self):
        if not self._size:
            self._size = sum((c.size for c in self.content))
        return self._size

    def cd(self, name: str):
        for item in self.content:
            if isinstance(item, Dir) and item.name == name:
                return item
        raise ValueError(f"Dir '{name}' not found")

    def get_directories_recurse(self) -> Generator['Dir', None, None]:
        yield self
        for item in self.content:
            if isinstance(item, Dir):
                yield from item.get_directories_recurse()

MAX_DIR_SIZE = 100_000

DRIVE_SIZE = 70_000_000
FREE_SPACE_NEEDED = 30_000_000

if __name__ == "__main__":
    ls = False
    puzzle = PuzzleInput(__file__).get()
    current = Dir("/")
    root = current
    lines = puzzle.splitlines()
    for line in lines[1:]:
        if line[0] == "$":
            ls = line == "$ ls"
            if not ls:
                if line == "$ cd ..":
                    current = current.parent
                elif line.startswith("$ cd "):
                    name = line[5:]
                    current = current.cd(name)
                else:
                    raise RuntimeError(F"invalid command: '{line}'")
        elif ls:
            size, name = line.split()
            new = Dir(name, current) if (size == "dir") else File(name, int(size))
            current.content.append(new)
        else:
            raise RuntimeError(f"invalid state")

    found = (dir for dir in root.get_directories_recurse() if dir.size <= MAX_DIR_SIZE)
    part_1 = sum((d.size for d in found))
    print(f"Part 1: {part_1}")

    needed = FREE_SPACE_NEEDED - (DRIVE_SIZE - root.size)
    to_delete: Dir = min((d for d in root.get_directories_recurse() if d.size >= needed), key=lambda x: x.size)
    print(f"Part 2: {to_delete.size}")
