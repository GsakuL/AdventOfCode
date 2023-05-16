from typing import List, NamedTuple, Dict, Any


class Vector2(NamedTuple):
    x: int
    y: int


class WrapMap:
    def __init__(self, data: List[str]) -> None:
        super().__init__()
        mapped = {}
        for y, line in enumerate(data):
            for x, letter in enumerate(line):
                mapped[Vector2(x, y)] = letter
        self.data: Dict[Vector2, Any] = mapped
        self.nil = object()
        self.size = Vector2(len(data[0]), len(data))

    def __getitem__(self, key: Vector2):
        adjusted = Vector2(key.x % self.size.x, key.y % self.size.y)
        return self.data[adjusted]
        value = self.data.get(key, self.nil)
        if value is not self.nil:
            return value
