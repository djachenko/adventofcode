from collections import defaultdict
from distutils.command.check import check

from utils import read_by_line, Field, Point

EMPTY = "."


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


def main():
    end: Point

    field, start, end = read_input()

    field.flood_fill(start)

    back_path = field.get_back_path(end)

    cheat_counts = defaultdict(lambda: 0)

    for point in back_path:
        current_value = field[point]

        for neighbour in point.n_neighbours(20):
            neighbour: Point
            neighbour_value = field[neighbour]

            if not isinstance(neighbour_value, int):
                continue

            diff = current_value - neighbour_value
            distance = neighbour.manhattan_from(point)

            cheat_value = diff - distance

            if cheat_value > 0:
                cheat_counts[cheat_value] += 1

    total_sum = 0

    for cheat_value, cheat_count in cheat_counts.items():
        if cheat_value >= 100:
            total_sum += cheat_count

    print(total_sum)


if __name__ == '__main__':
    main()
