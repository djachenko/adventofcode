from utils import read_by_line, Field, Point, Direction


def main():
    field = Field()
    boxes = set()
    robot = None

    stream = read_by_line()

    for y, line in enumerate(stream):
        line = line.strip()

        if not line:
            break

        for x, cell in enumerate(line):
            if cell == "@":
                robot = Point(x, y)
                cell = "."
            elif cell == "O":
                boxes.add(Point(x, y))
                cell = "."

            field[x, y] = cell

    moves = []

    for line in stream:
        line = line.strip()

        for c in line:
            moves.append(Direction.parse(c))

    def check_next_cell(point: Point, direction: Direction) -> bool:
        if field[point] == "#":
            return False

        if point in boxes:
            next_point = point + direction

            check = check_next_cell(next_point, direction)

            if check:
                boxes.remove(point)
                boxes.add(next_point)

            return check

        return True

    for move in moves:
        next_robot = robot + move

        if check_next_cell(next_robot, move):
            robot = next_robot

    gps_sum = 0

    for box in boxes:
        box_gps = box.x + 100 * box.y

        gps_sum += box_gps

    print(gps_sum)


if __name__ == '__main__':
    main()
