from dataclasses import dataclass
from enum import Enum
from functools import lru_cache

from math import log10
from pathlib import Path
from typing import Tuple, Iterable, List, TypeVar, Callable


def split_int(a: int) -> (int, int):
    length = length_of_int(a)

    splitter = pow(10, length / 2)

    return int(a / splitter), int(a % splitter)


def length_of_int(a: int) -> int:
    if a == 0:
        return 1

    return int(log10(a)) + 1


class Direction(Enum):
    UP = 0, -1, "^"
    RIGHT = 1, 0, ">"
    DOWN = 0, 1, "V"
    LEFT = -1, 0, "<"

    def __init__(self, dx: int, dy: int, representation: str):
        self.dx = dx
        self.dy = dy

        self.__representation = representation

    @staticmethod
    def parse(string: str):
        for direction in Direction:
            if str(direction) == string:
                return direction

        return None

    @staticmethod
    def from_dx_dy(dx: int, dy: int) -> 'Direction':
        for d in Direction:
            if d.dx == dx and d.dy == dy:
                return d

    @staticmethod
    @lru_cache()
    def representations() -> List[str]:
        return [str(d) for d in Direction]

    def __str__(self) -> str:
        return self.__representation

    def next(self) -> 'Direction':
        if self == Direction.UP:
            return Direction.RIGHT

        if self == Direction.RIGHT:
            return Direction.DOWN

        if self == Direction.DOWN:
            return Direction.LEFT

        if self == Direction.LEFT:
            return Direction.UP


@dataclass
class Point:
    x: int
    y: int

    def __iter__(self):
        yield self.x
        yield self.y

    @property
    @lru_cache()
    def neighbours(self) -> List['Point']:
        return [self + direction for direction in Direction]

    def is_neighbour_of(self, other: 'Point') -> bool:
        return other in self.neighbours

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        x, y = other

        return self.x == x and self.y == other.y

    def __mul__(self, factor: int) -> 'Point':
        return Point(self.x * factor, self.y * factor)

    def __add__(self, other) -> 'Point':
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, Direction):
            return Point(self.x + other.dx, self.y + other.dy)

    @staticmethod
    def from_tuple(t: Tuple[int, int]) -> 'Point':
        return Point(t[0], t[1])


Coordinate = Tuple[int, int] | Point


class Field:
    @property
    def height(self):
        if not self.__field:
            return 0

        return max(y for _, y in self.__field) + 1

    @property
    def width(self):
        if not self.__field:
            return 0

        return max(x for x, _ in self.__field) + 1

    def __init__(self, default_factory=lambda: None):
        self.__field = {}
        self.__factory = default_factory

    def __getitem__(self, coordinate: Coordinate):
        x, y = coordinate

        if (x, y) not in self.__field:
            return self.__factory()

        return self.__field[x, y]

    def __setitem__(self, coordinate: Coordinate, value):
        x, y = coordinate

        self.__field[x, y] = value

    def __iter__(self):
        return iter(self.__field)

    def __str__(self):
        lines = []

        for y in range(-1, self.height):
            cells = []

            for x in range(-1, self.width):
                cell = str(self[x, y])
                cells.append(cell)

            line = "".join(cells)
            lines.append(line)

        result = "\n".join(lines)

        return result

    @staticmethod
    def read(stream: Iterable[str], default_factory=lambda: None, converter=lambda x: x) -> 'Field':
        field = Field(default_factory)

        for y, line in enumerate(stream):
            line = line.strip()

            for x, cell in enumerate(line):
                field[x, y] = converter(cell)

        return field


INPUT_FILE = Path("input.txt")


def read_by_line() -> Iterable[str]:
    with INPUT_FILE.open() as input_file:
        for line in input_file:
            yield line.strip()


def read_single_line() -> str:
    with INPUT_FILE.open() as input_file:
        return input_file.read()


T = TypeVar("T")


def first(seq: Iterable[T], criteria: Callable[[T], bool] = lambda: True) -> T | None:
    for i in seq:
        if criteria(i):
            return i

    return None


def chunks(seq: List[T], n: int) -> Iterable[List[T]]:
    for i in range(0, len(seq), n):
        yield seq[i:i + n]
