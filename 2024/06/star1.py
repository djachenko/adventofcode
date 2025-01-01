from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Tuple, List, Dict


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


def field_contains(field: Dict[Tuple[int, int], str], x: int, y: int) -> bool:
    return (x, y) in field.keys()


FIELD_SIZE = 10


def print_field(field: Dict[Tuple[int, int], str]):
    for y in range(FIELD_SIZE):
        for x in range(FIELD_SIZE):
            print(field[x, y], end="")

        print()

    print()
    print()


@dataclass
class Guard:
    x: int
    y: int
    direction: Direction

    def next_step(self) -> Tuple[int, int]:
        return self.x + self.direction.dx, self.y + self.direction.dy

    def turn(self):
        self.direction = self.direction.next()

    def move(self):
        self.x += self.direction.dx
        self.y += self.direction.dy


VISITED = "X"
EMPTY = "."
OBSTACLE = "#"


def main():
    with Path("input.txt").open() as input_file:
        field = {}

        guard = None

        for y, line in enumerate(input_file):
            for x, cell in enumerate(line):
                if cell in Direction.representations():
                    guard = Guard(x, y, Direction.parse(cell))

                    cell = "."

                field[x, y] = cell

    field[guard.x, guard.y] = VISITED

    while True:
        x, y = guard.next_step()

        if not field_contains(field, x, y):
            break

        if field[x, y] == OBSTACLE:
            guard.turn()
        else:
            guard.move()
            field[guard.x, guard.y] = VISITED

    visited_cells = [cell for cell in field.values() if cell == VISITED]

    print(len(visited_cells))


if __name__ == '__main__':
    main()
