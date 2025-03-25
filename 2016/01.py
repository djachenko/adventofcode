from framework.aoc import *
from utils.structures import Direction, Point

INSTRUCTIONS = INPUT.line.split(", ")


def __parse_command(direction: Direction, instruction: str) -> (Direction, int):
    command = instruction[0]
    step_count = int(instruction[1:])

    if command == "R":
        direction = direction.clockwise()
    elif command == "L":
        direction = direction.counterclockwise()
    else:
        assert False

    return direction, step_count


def star1() -> Output:
    direction = Direction.UP
    point = Point.zero()

    for instruction in INSTRUCTIONS:
        direction, step_count = __parse_command(direction, instruction)

        point += direction * step_count

    return point.manhattan()


def star2() -> Output:
    direction = Direction.UP
    point = Point.zero()

    visited_points = {point}

    for instruction in INSTRUCTIONS:
        direction, step_count = __parse_command(direction, instruction)

        for _ in range(step_count):
            point = point + direction

            if point not in visited_points:
                visited_points.add(point)
            else:
                return point.manhattan()


if __name__ == '__main__':
    run(star1, star2)
