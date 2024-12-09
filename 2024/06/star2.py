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


def get_field_size(field: Dict[Tuple[int, int], str]) -> Tuple[int, int]:
    max_x = 0
    max_y = 0

    for x, y in field.keys():
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    return max_x + 1, max_y + 1


def print_field(field: Dict[Tuple[int, int], str]):
    width, height = get_field_size(field)

    for y in range(height):
        for x in range(width):
            print(field[x, y], end="")

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
NEW_OBSTACLE = "O"


def main():
    with Path("input.txt").open() as input_file:
        field = {}

        guard: Guard

        for next_y, line in enumerate(input_file):
            line = line.strip()

            for next_x, cell in enumerate(line):
                if cell in Direction.representations():
                    guard = Guard(next_x, next_y, Direction.parse(cell))

                    cell = EMPTY

                field[next_x, next_y] = cell

    count = 0

    for obstacle_x, obstacle_y in field.keys():
        if field[obstacle_x, obstacle_y] is not EMPTY:
            continue

        local_field = field.copy()
        local_field[obstacle_x, obstacle_y] = NEW_OBSTACLE

        x = guard.x
        local_guard = Guard(x, guard.y, guard.direction)

        while True:
            guard_direction = str(local_guard.direction)

            current_x = local_guard.x
            current_y = local_guard.y

            if local_field[current_x, current_y] == guard_direction:
                count += 1

                break

            next_x, next_y = local_guard.next_step()

            if not field_contains(local_field, next_x, next_y):
                break

            next_cell = local_field[next_x, next_y]

            if next_cell == OBSTACLE or next_cell == NEW_OBSTACLE:
                if local_field[current_x, current_y] == EMPTY:
                    local_field[current_x, current_y] = guard_direction

                local_guard.turn()
            else:
                if local_field[current_x, current_y] == EMPTY:
                    local_field[current_x, current_y] = guard_direction

                local_guard.move()

    print(count)


if __name__ == '__main__':
    main()
