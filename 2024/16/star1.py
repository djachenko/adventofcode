from dataclasses import dataclass

from utils import read_by_line, Field, Point, Direction

EMPTY = "."
WALL = "#"


@dataclass
class Deer:
    point: Point
    direction: Direction


def main():
    start = None
    end = None

    field = Field()

    stream = read_by_line()

    for y, line in enumerate(stream):
        for x, cell in enumerate(line):
            if cell == "S":
                start = Point(x, y)
                cell = EMPTY
            elif cell == "E":
                end = Point(x, y)
                cell = EMPTY

            field[x, y] = cell

    queue = [(Deer(start, Direction.RIGHT), 0)]

    while queue:
        deer, price = queue.pop(0)

        current_cell = field[deer.point]

        if current_cell == WALL:
            continue

        if current_cell == EMPTY or current_cell > price:
            field[deer.point] = price

            next_price = price + 1
            next_direction = deer.direction
            next_step = deer.point + next_direction
            next_deer = Deer(next_step, next_direction)

            side_price = price + 1001

            left_direction = deer.direction.counterclockwise()
            left_step = deer.point + left_direction
            left_deer = Deer(left_step, left_direction)

            right_direction = deer.direction.clockwise()
            right_step = deer.point + right_direction
            right_deer = Deer(right_step, right_direction)

            queue += [
                (next_deer, next_price),
                (left_deer, side_price),
                (right_deer, side_price),
            ]

    print(field[end])


if __name__ == '__main__':
    main()
