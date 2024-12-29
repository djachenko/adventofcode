from dataclasses import dataclass
from enum import Enum
from functools import lru_cache

from math import log10
from pathlib import Path
from typing import Tuple, Iterable, List, TypeVar, Callable, Dict


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
            if str(direction).lower() == string.lower():
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

    def counterclockwise(self) -> 'Direction':
        if self == Direction.UP:
            return Direction.LEFT

        if self == Direction.RIGHT:
            return Direction.UP

        if self == Direction.DOWN:
            return Direction.RIGHT

        if self == Direction.LEFT:
            return Direction.DOWN

    def clockwise(self) -> 'Direction':
        return self.next()

    def reverse(self) -> 'Direction':
        return Direction.from_dx_dy(self.dx * -1, self.dy * -1)


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

    @lru_cache()
    def n_neighbours(self, n: int) -> List['Point']:
        result = []

        for dx in range(-n, n + 1):
            abs_dx = abs(dx)

            for dy in range(-n + abs_dx, n - abs_dx + 1):
                if dx == 0 and dy == 0:
                    continue

                result.append(Point(self.x + dx, self.y + dy))

        return result

    def is_neighbour_of(self, other: 'Point', distance: int = 1) -> bool:
        if self == other:
            return False

        return self.manhattan_from(other) <= distance

    def manhattan_from(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        x, y = other

        return self.x == x and self.y == y

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
    WALL = "#"
    EMPTY = "."

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

        for y in range(self.height):
            cells = []

            for x in range(self.width):
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

    def flood_fill(self, start: Point) -> None:
        queue = [(start, 0)]

        while queue:
            point, generation = queue.pop(0)

            if point not in self:
                continue

            if self[point] == Field.WALL:
                continue

            if self[point] == Field.EMPTY:
                self[point] = generation

                queue += [(neighbour, generation + 1) for neighbour in point.neighbours]

    def get_all_back_paths_cells(self, end: Point) -> List[Point]:
        path = [end]

        next_generation = path.copy()

        while next_generation:
            prev_generation = next_generation
            next_generation = []

            for point in prev_generation:
                current_cell = self[point]

                for neighbour in point.neighbours:
                    neighbour_cell = self[neighbour]

                    if neighbour_cell == Field.WALL:
                        continue

                    if neighbour_cell == current_cell - 1:
                        next_generation.append(neighbour)

            path += next_generation

        return path

    def get_back_path(self, end: Point) -> List[Point]:
        path = [end]

        while True:
            current_point = path[-1]
            current_cell = self[current_point]

            if current_cell == 0:
                break

            for neighbour in current_point.neighbours:
                neighbour_cell = self[neighbour]

                if neighbour_cell == Field.WALL:
                    continue

                if neighbour_cell == current_cell - 1:
                    path.append(neighbour)

                    break

            assert path[-1] != current_point

        return path


INPUT_FILE = Path("input.txt")


def read_by_line() -> Iterable[str]:
    with INPUT_FILE.open() as input_file:
        for line in input_file:
            yield line.strip()


def read_single_line() -> str:
    with INPUT_FILE.open() as input_file:
        return input_file.read()


class Input:
    def __init__(self, file_name: str) -> None:
        super().__init__()

        self.__path = Path(file_name)

    @property
    @lru_cache()
    def line(self) -> str:
        with self.__path.open() as input_file:
            return input_file.read()

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


INPUT = Input("input.txt")

T = TypeVar("T")
V = TypeVar("V")


def first(seq: Iterable[T], criteria: Callable[[T], bool] = lambda: True) -> T | None:
    for i in seq:
        if criteria(i):
            return i

    return None


def chunks(seq: List[T], n: int) -> Iterable[List[T]]:
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def reverse_dict(d: Dict[T, V]) -> Dict[V, List[T]]:
    result = {}

    for key, value in d.items():
        if value not in result:
            result[value] = []

        result[value].append(key)

    return result


def unique(s: Iterable[T]) -> List[T]:
    cache = set()
    unique_s = []

    for e in s:
        if e in cache:
            continue

        cache.add(e)
        unique_s.append(e)

    return unique_s


def find(seq: List[T], predicate: Callable[[T], bool]) -> T | None:
    return next(filter(predicate, seq), None)
