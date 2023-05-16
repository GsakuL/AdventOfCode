import os
from enum import Flag
from typing import Callable, Dict, Optional, Tuple, Union

_nil = object()

BorderType = Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int, int]]


class Transform(Flag):
    NONE = 0
    FLIP_HORIZONTAL = 2 ** 0
    FLIP_VERTICAL = 2 ** 1
    FLIP_BOTH = FLIP_HORIZONTAL | FLIP_VERTICAL
    ORIGIN_TOP_LEFT = FLIP_HORIZONTAL
    ORIGIN_CENTER = NONE


class Screen:
    """
    A dict wrapper for IntCode-Programs
    """
    FULL_BLOCK = "█"
    BORDER_CHAR = " "

    def __init__(self, char_map: Optional[Dict[Union[str, int], Union[str, int]]] = None,
                 pixels: Optional[Dict[Tuple[int, int], Union[str, int]]] = None,
                 default: Union[str, int, None] = _nil, transform: Transform = Transform.NONE,
                 overlay: Optional[Union[dict, Callable[[], Dict]]] = None, immediate: bool = False,
                 border: Optional[BorderType] = None, suppress_paint: bool = False):
        self.pixels = dict()
        self.mapping = char_map or dict()
        self._default = default
        self.max_y = self.max_x = -float('inf')
        self.min_y = self.min_x = float('inf')
        self.transform = transform
        self.get_overlay = self._overlay(overlay)
        self.immediate = immediate
        self.border = self._border(border)
        self.suppress_paint = suppress_paint
        if pixels:
            for k, v in pixels.items():
                self[k] = v
        self.dirty = True
        self.last_overlay = self.get_overlay()

    @staticmethod
    def _overlay(ov) -> Callable[[], dict]:
        if not ov:
            ov = {}
        if isinstance(ov, dict):
            return lambda: ov
        return ov

    @staticmethod
    def _border(border: Optional[BorderType]) -> Tuple[int, int, int, int]:
        if not border:
            border = (0,)
        if isinstance(border, int):
            border = (border,)
        length = len(border)
        if length == 1:
            return border[0], border[0], border[0], border[0]
        if length == 2:
            return border[0], border[1], border[0], border[1]  # type: ignore
        if length == 4:
            return border[0], border[1], border[2], border[3]  # type: ignore
        raise ValueError(f"invalid border format: '{border}")

    def __setitem__(self, key, value):
        x, y = key
        g = self.pixels.get((x, y), _nil)
        if g != value:
            self.update_min_max(x, y)
            self.pixels[(x, y)] = value
            self.dirty = True
            self.paint_immediate()

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_min_max(self, x, y):
        if x < self.min_x:
            self.min_x = x
        if y < self.min_y:
            self.min_y = y
        if x > self.max_x:
            self.max_x = x
        if y > self.max_y:
            self.max_y = y

    def __getitem__(self, item):
        item = tuple(item)
        i = self.pixels.get(item, self._default)
        if i is _nil:
            raise KeyError(f"item '{item}' not found")
        return i

    def __repr__(self):
        return f"Screen<w:{self.width} h:{self.height}>"

    __str__ = __repr__

    def find(self, pixel: Union[str, int]):
        return ((k, v) for k, v in self.pixels.items() if v == pixel)

    def paint_immediate(self):
        if self.immediate:
            self.clear()
            self.paint()

    @property
    def width(self):
        try:
            return int(self.max_x - self.min_x)
        except OverflowError:
            return 0

    @property
    def height(self):
        try:
            return int(self.max_y - self.min_y)
        except OverflowError:
            return 0

    def clean(self):
        for k in self.pixels:
            self.pixels[k] = self._default
        self.paint_immediate()

    def wipe(self):
        self.pixels.clear()
        self.paint_immediate()

    def construct(self,  enable_overlay: bool = True, enable_char_map: bool = True):
        ov = self.get_overlay() if enable_overlay else {}
        cm = self.mapping if enable_char_map else {}
        if (not self.width) and (not self.height):
            return []
        out = []
        for y in range(int(self.max_y), int(self.min_y) - 1, -1):
            line = ""
            for x in range(int(self.min_x), int(self.max_x) + 1):
                c = ov.get((x, y), self.pixels.get((x, y), self._default))
                line += str(cm.get(c, c))
            if Transform.FLIP_VERTICAL in self.transform:
                line = str(reversed(line))
            out.append((self.BORDER_CHAR * self.border[3]) + line + (self.BORDER_CHAR * self.border[1]))
        if Transform.FLIP_HORIZONTAL in self.transform:
            out = list(reversed(out))
        return (([self.BORDER_CHAR * self.width] * self.border[0]) + out
                + ([self.BORDER_CHAR * self.width] * self.border[2]))

    def paint(self, force: bool = False, enable_overlay: bool = True, enable_char_map: bool = True):
        if force or (self.dirty and not self.suppress_paint):
            o = self.get_overlay().copy()
            if self.last_overlay != 0:
                self.dirty = True
                self.last_overlay = o
                for k in o:
                    self.update_min_max(*k)
            print("\n".join(self.construct(enable_overlay=enable_overlay, enable_char_map=enable_char_map)))
            self.dirty = False
            return True
        return False
