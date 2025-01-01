from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from PIL import Image

from utils import read_by_line, Point

FIELD_WIDTH = 101
FIELD_HEIGHT = 103

ITERATIONS = 10000


@dataclass
class Robot:
    point: Point
    velocity: Point

    def move(self) -> None:
        self.point += self.velocity

        self.point.x %= FIELD_WIDTH
        self.point.y %= FIELD_HEIGHT


def field_string(robots: List[Robot]) -> str:
    lines = []

    for y in range(FIELD_HEIGHT):
        line = []

        for x in range(FIELD_WIDTH):
            robots_count = 0

            for robot in robots:
                if robot.point.x == x and robot.point.y == y:
                    robots_count += 1

            if robots_count > 0:
                line.append(str(robots_count))
            else:
                line.append(".")

        lines.append("".join(line))

    return "\n".join(lines)


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


def generate_image(robots: List[Robot]):
    pixel_size = 2

    image = Image.new(mode="1", size=(pixel_size * FIELD_WIDTH, pixel_size * FIELD_HEIGHT))
    pixel_values = defaultdict(lambda: 0)

    for robot in robots:
        pixel_values[robot.point.x, robot.point.y] = 1

    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            pixel = pixel_values[x, y]

            x_start = x * pixel_size
            y_start = y * pixel_size

            x_end = x_start + pixel_size
            y_end = y_start + pixel_size

            for pixel_x in range(x_start, x_end):
                for pixel_y in range(y_start, y_end):
                    image.putpixel((pixel_x, pixel_y), pixel)

    return image


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

    easter_folder = Path("easter_egg")
    easter_folder.mkdir(exist_ok=True)

    for i in range(ITERATIONS):
        print(i)

        for robot in robots:
            robot.move()

        image = generate_image(robots)
        image.save(easter_folder / f"iter_{i + 1}.jpg")


if __name__ == '__main__':
    main()
