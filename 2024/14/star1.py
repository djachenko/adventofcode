from dataclasses import dataclass
from typing import List, Tuple

from utils import read_by_line, Point

FIELD_WIDTH = 101
FIELD_HEIGHT = 103

ITERATIONS = 100


@dataclass
class Robot:
    point: Point
    velocity: Point

    def move(self) -> None:
        self.point += self.velocity

        self.point.x %= FIELD_WIDTH
        self.point.y %= FIELD_HEIGHT


def print_robots(robots: List[Robot]) -> None:
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            robots_count = 0

            for robot in robots:
                if robot.point.x == x and robot.point.y == y:
                    robots_count += 1

            if robots_count > 0:
                print(robots_count, end="")
            else:
                print(".", end="")

        print()
    print()


def count_robots(quadrant: List[Tuple[int, int]], robots: List[Robot]) -> int:
    count = 0

    for x, y in quadrant:
        for robot in robots:
            if robot.point.x == x and robot.point.y == y:
                count += 1

    return count


def main():
    robots = []

    for line in read_by_line():
        point_line, velocity_line = line.split(" ")

        point_line = point_line.split("=")[1]
        x, y = [int(i) for i in point_line.split(",")]

        velocity_line = velocity_line.split("=")[1]
        dx, dy = [int(i) for i in velocity_line.split(",")]

        robot = Robot(Point(x, y), Point(dx, dy))

        robots.append(robot)

    for i in range(ITERATIONS):
        for robot in robots:
            robot.move()

    print_robots(robots)

    mid_x = FIELD_WIDTH // 2
    mid_y = FIELD_HEIGHT // 2

    first_quadrant = []

    for y in range(mid_y):
        for x in range(mid_x):
            first_quadrant.append((x, y))

    second_quadrant = []

    for y in range(mid_y):
        for x in range(mid_x + 1, FIELD_WIDTH):
            second_quadrant.append((x, y))

    third_quadrant = []

    for y in range(mid_y + 1, FIELD_HEIGHT):
        for x in range(mid_x):
            third_quadrant.append((x, y))

    fourth_quadrant = []

    for y in range(mid_y + 1, FIELD_HEIGHT):
        for x in range(mid_x + 1, FIELD_WIDTH):
            fourth_quadrant.append((x, y))

    first_count = count_robots(first_quadrant, robots)
    second_count = count_robots(second_quadrant, robots)
    third_count = count_robots(third_quadrant, robots)
    fourth_count = count_robots(fourth_quadrant, robots)

    result = first_count * second_count * third_count * fourth_count

    print(result)


if __name__ == '__main__':
    main()
