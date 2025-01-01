from utils import read_by_line, Field, Point

EMPTY = "."
WALL = "#"

FIELD_SIZE = 71


def main():
    field = Field(default_factory=lambda: EMPTY)

    for y in range(FIELD_SIZE):
        for x in range(FIELD_SIZE):
            field[x, y] = EMPTY

    bytes_to_fall = []

    for line in read_by_line():
        x, y = [int(i) for i in line.split(",")]

        bytes_to_fall.append(Point(x, y))

    for byte in bytes_to_fall[:1024]:
        field[byte] = WALL

    start = Point(0, 0)
    end = Point(FIELD_SIZE - 1, FIELD_SIZE - 1)

    field[start] = 0

    for generation, byte_point in enumerate(bytes_to_fall):
        if isinstance(field[end], int):
            break

        points_of_generation = []

        for point in field:
            if field[point] == generation:
                points_of_generation.append(Point.from_tuple(point))

        next_generation = generation + 1

        for point in points_of_generation:
            for neighbour in point.neighbours:
                if neighbour not in field:
                    continue

                neighbour_cell = field[neighbour]

                if neighbour_cell == WALL:
                    continue

                if neighbour_cell == EMPTY or neighbour_cell > next_generation:
                    field[neighbour] = next_generation

    print(field[end])


if __name__ == '__main__':
    main()
