from copy import copy
from typing import List

from framework.aoc import *
from utils.funcs import count_if
from utils.structures import Field, Point

FIELD = INPUT.field()
STEPS = 100

ON = Field.WALL
OFF = Field.EMPTY


def __life(eternal_points: List[Point]) -> Output:
    next_field = copy(FIELD)
    current_field = copy(FIELD)

    for point in eternal_points:
        current_field[point] = ON
        next_field[point] = ON

    for step in range(STEPS):
        for point in FIELD:
            point = Point.from_tuple(point)

            count = count_if(point.neighbours_8, lambda n: current_field[n] == ON)

            current_state = current_field[point] == ON

            if current_state:
                new_state = (count == 2 or count == 3)
            else:
                new_state = (count == 3)

            if new_state:
                new_cell = ON
            else:
                new_cell = OFF

            next_field[point] = new_cell

        for point in eternal_points:
            next_field[point] = ON

        current_field, next_field = next_field, current_field

    return count_if(current_field, lambda p: current_field[p] == ON)


def star1() -> Output:
    return __life([])


def star2() -> Output:
    return __life([
        Point(0, 0),
        Point(0, FIELD.height - 1),
        Point(FIELD.width - 1, 0),
        Point(FIELD.width - 1, FIELD.height - 1),
    ])


if __name__ == '__main__':
    run(star1, star2)
