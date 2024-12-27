from dataclasses import dataclass
from typing import List, Tuple

from utils import read_by_line, Field, Point, Direction, unique

EMPTY = "."
WALL = "#"

MAX_PRICE = 9999999999


@dataclass
class Deer:
    point: Point
    direction: Direction


def read_input() -> (Field, Point, Point):
    start = None
    end = None

    field = Field()

    stream = read_by_line()

    for y, line in enumerate(stream):
        for x, current_point in enumerate(line):
            if current_point == "S":
                start = Point(x, y)
                current_point = EMPTY
            elif current_point == "E":
                end = Point(x, y)
                current_point = EMPTY

            field[x, y] = current_point

    return field, start, end


def forward(field: Field, start: Point) -> None:
    queue = [(Deer(start, Direction.RIGHT), 0)]

    while queue:
        deer, current_price = queue.pop(0)

        deer_point = deer.point
        deer_direction = deer.direction

        current_cell = field[deer_point]

        if current_cell == WALL:
            continue

        if current_cell == EMPTY:
            current_cell = {d: MAX_PRICE for d in Direction}

        if current_cell[deer_direction] > current_price:
            current_cell[deer_direction] = current_price

            forward_price = current_price + 1
            forward_direction = deer_direction
            forward_step = deer_point + forward_direction
            forward_deer = Deer(forward_step, forward_direction)

            side_price = current_price + 1001

            left_direction = deer_direction.counterclockwise()
            left_step = deer_point + left_direction
            left_deer = Deer(left_step, left_direction)

            right_direction = deer_direction.clockwise()
            right_step = deer_point + right_direction
            right_deer = Deer(right_step, right_direction)

            queue += [
                (forward_deer, forward_price),
                (left_deer, side_price),
                (right_deer, side_price),
            ]

        field[deer_point] = current_cell


def reverse_directions(field: Field) -> None:
    for current_point in field:
        cell = field[current_point]

        if not isinstance(cell, dict):
            continue

        field[current_point] = {d.reverse(): p for d, p in cell.items() if p < MAX_PRICE}


def backwards(field: Field, end: Point) -> List[Point]:
    best_places = [(end, d) for d in field[end]]
    next_generation = best_places.copy()

    while next_generation:
        prev_generation: List[Tuple[Point, Direction]] = next_generation
        next_generation = []

        for current_point, current_direction in prev_generation:
            current_cell = field[current_point]
            current_price = current_cell[current_direction]

            next_point = current_point + current_direction
            next_cell = field[next_point]

            if isinstance(next_cell, dict):
                fw_direction = current_direction
                cw_direction = current_direction.clockwise()
                ccw_direction = current_direction.counterclockwise()

                if next_cell.get(fw_direction, MAX_PRICE) == current_price - 1:
                    next_generation.append((next_point, fw_direction))

                if next_cell.get(cw_direction, MAX_PRICE) == current_price - 1001:
                    next_generation.append((next_point, cw_direction))

                if next_cell.get(ccw_direction, MAX_PRICE) == current_price - 1001:
                    next_generation.append((next_point, ccw_direction))

        next_generation = unique(next_generation)

        best_places += next_generation

    return unique(point for point, _ in best_places)


def main():
    field, start, end = read_input()

    forward(field, start)

    reverse_directions(field)

    best_price = min(field[end].values())

    field[end] = {d: p for d, p in field[end].items() if p == best_price}

    best_places = backwards(field, end)

    print(len(best_places))


if __name__ == '__main__':
    main()
