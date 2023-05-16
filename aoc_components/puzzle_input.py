import re
from os import path
import requests
import pathlib
from typing import overload, Union, Optional, List, Any, Callable

__all__ = ["PuzzleInput"]


class PuzzleInput:
    @overload
    def __init__(self, a: int, b: int, *, encoding: str = "utf8") -> None:
        ...

    @overload
    def __init__(self, a: str, *, encoding: str = "utf8") -> None:
        ...

    @overload
    def __init__(self, a: Union[str, int], b: Optional[int] = None, *, encoding: str = "utf8") -> None:
        ...

    def __init__(self, a: Union[str, int], b: Optional[int] = None, *, encoding: str = "utf8"):
        if isinstance(a, str) and not b:
            year, day = self._get_date_code(a)
        else:
            if (not isinstance(a, int)) or (not isinstance(b, int)):
                raise TypeError()
            year, day = a, b
            if day > year:
                year, day = day, year

        assert day in range(1, 26)
        assert year >= 2015

        self.day = day
        self.year = year
        self.file = pathlib.Path(str(year)) / "input" / f"{day:02d}.txt"
        self.encoding = encoding

    @property
    def url(self):
        """api doesn't use leading zeros"""
        return f"https://adventofcode.com/{self.year}/day/{self.day}/input"

    @staticmethod
    def _get_date_code(file_path: str):
        file = pathlib.Path(file_path)
        year = file.parent.name
        m = re.match(r"[a-zA-Z_-]*(\d+)[a-zA-Z_-]*\.py", file.name)
        if not m:
            raise RuntimeError()
        day = m[1]
        return int(year), int(day)

    @staticmethod
    def get_cookies():
        cookie_path = pathlib.Path("aoc_components") / "_session_cookie.txt"
        if cookie_path.is_file():
            with cookie_path.open("r") as fp:
                sc = fp.read()
            if sc:
                cookies = {"session": sc}
                return cookies
        raise FileNotFoundError(f"please supply your session cookie in {path.abspath(cookie_path)}")

    def download(self):
        self.file.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(self.url, cookies=self.get_cookies())
        r.encoding = self.encoding
        if r.status_code != requests.codes.ok:
            raise requests.ConnectionError(f"cannot get '{self.url}'. Error: {r.status_code} {r.text}")
        text = r.text
        with self.file.open("w", encoding=self.encoding) as fp:
            fp.write(text)
        return text

    def get(self):
        if not self.file.is_file():
            return self.download()
        with self.file.open("r", encoding=self.encoding) as fp:
            return fp.read()

    def __call__(self, *args: Any, **kwds: Any) -> str:
        if (any(args) or any(kwds)):
            raise RuntimeError("no parameters allowed")
        return self.get()

    def as_list(self, delim: str = ",", cast: Optional[Callable[[Any], Any]] = None):
        items: List[Any] = self.get().split(delim)
        if cast:
            items = [cast(i) for i in items]
        return items
