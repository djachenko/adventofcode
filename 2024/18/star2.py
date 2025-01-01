from utils import read_by_line, Field, Point

EMPTY = "."
WALL = "#"
VISITED = "x"

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

    start = Point(0, 0)
    end = Point(FIELD_SIZE - 1, FIELD_SIZE - 1)

    min_generation = 1024
    max_generation = len(bytes_to_fall)

    while max_generation - min_generation > 1:
        generation = (max_generation + min_generation) // 2
        generation_bytes = bytes_to_fall[:generation]

        for point in generation_bytes:
            field[point] = WALL

        queue = [start]
        visited_points = []

        while queue and field[end] != VISITED:
            point = queue.pop(0)

            if point not in field:
                continue

            if field[point] == WALL:
                continue

            if field[point] == EMPTY:
                field[point] = VISITED

                visited_points.append(point)

                queue += point.neighbours

        print(generation, field[end], generation_bytes[-1])

        if field[end] == VISITED:
            min_generation = generation
        elif field[end] == EMPTY:
            max_generation = generation

        for point in generation_bytes:
            field[point] = EMPTY

        for point in visited_points:
            field[point] = EMPTY


if __name__ == '__main__':
    main()
