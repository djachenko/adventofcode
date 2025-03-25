import os
from abc import abstractmethod
from functools import lru_cache
from pathlib import Path
from typing import List

from requests_cache import CachedSession, DEFAULT_CACHE_NAME

from utils.structures import Field, Point


class Input:
    @property
    @abstractmethod
    def line(self) -> str:
        return ""

    @property
    def lines(self) -> List[str]:
        return self.line.split("\n")

    @property
    def blocks(self) -> List[List[str]]:
        return [block.split("\n") for block in self.line.split("\n\n")]

    def field(self) -> Field:
        field_, start, end = self.field_se()

        assert start is None
        assert end is None

        return field_

    @lru_cache()
    def field_se(self) -> (Field, Point | None, Point | None):
        field_ = Field()
        start = None
        end = None

        for y, line in enumerate(self.lines):
            for x, cell in enumerate(line):
                if cell == "S":
                    start = Point(x, y)
                    cell = Field.EMPTY

                if cell == "E":
                    end = Point(x, y)
                    cell = Field.EMPTY

                field_[x, y] = cell

        return field_, start, end


class StringInput(Input):
    def __init__(self, string: str):
        self.__string = string.strip()

    @property
    def line(self) -> str:
        return self.__string


class FileInput(Input):
    def __init__(self, file_name: str) -> None:
        super().__init__()

        self.__path = Path(file_name)

    @property
    @lru_cache()
    def line(self) -> str:
        with self.__path.open() as input_file:
            return input_file.read()


class WebInput(Input):
    def __init__(self, year: int, day: int):
        self.__url = f"https://adventofcode.com/{year}/day/{day}/input"

    @property
    def line(self) -> str:
        response = WebInput.__session().get(self.__url, cookies={
            "session": WebInput.__cookie()
        })

        text = response.text
        text = text.strip()

        return text

    @staticmethod
    def __cookie() -> str:
        return os.environ["AOC_COOKIE"]

    @staticmethod
    def __session() -> CachedSession:
        cache_name = Path.cwd().parent / DEFAULT_CACHE_NAME

        session = CachedSession(cache_name=cache_name)

        return session
