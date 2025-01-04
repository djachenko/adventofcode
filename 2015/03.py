from copy import copy

from framework.aoc import *
from utils.structures import Point, Direction


def star1() -> Output:
    point = Point.zero()
    visited_points = {point}

    for char in INPUT.line:
        direction = Direction.parse(char)

        point = point + direction

        visited_points.add(point)

    return len(visited_points)


def star2() -> Output:
    point1 = Point.zero()
    point2 = copy(point1)

    visited_points = {point1}

    for char in INPUT.line:
        direction = Direction.parse(char)

        point1 = point1 + direction

        visited_points.add(point1)

        point1, point2 = point2, point1

    return len(visited_points)


if __name__ == '__main__':
    run(star1, star2)
