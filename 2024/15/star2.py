from utils import read_by_line, Field, Point, Direction


class WideBox:
    def __init__(self, point: Point):
        self.points = [
            point,
            Point(point.x + 1, point.y)
        ]

    def __add__(self, other) -> 'WideBox':
        return WideBox(self.points[0] + other)

    def __getitem__(self, point: Point):
        if point == self.points[0]:
            return "["
        elif point == self.points[1]:
            return "]"

        return None

    @property
    def x(self) -> int:
        return self.points[0].x

    @property
    def y(self) -> int:
        return self.points[0].y

    def __repr__(self):
        return repr(self.points)


def main():
    field = Field()
    boxes = []
    robot = None

    stream = read_by_line()

    for y, line in enumerate(stream):
        line = line.strip()

        if not line:
            break

        for x, cell in enumerate(line):
            if cell == "@":
                robot = Point(x * 2, y)
                cell = "."
            elif cell == "O":
                boxes.append(WideBox(Point(x * 2, y)))
                cell = "."

            field[x * 2, y] = cell
            field[x * 2 + 1, y] = cell

    moves = []

    for line in stream:
        line = line.strip()

        for c in line:
            moves.append(Direction.parse(c))

    def push(point: Point, move: Direction):
        for box in boxes:
            if point in box.points:
                next_box = box + move

                if move == Direction.LEFT:
                    push(next_box.points[0], move)
                elif move == Direction.RIGHT:
                    push(next_box.points[1], move)
                else:
                    for next_point in next_box.points:
                        push(next_point, move)

                boxes.remove(box)
                boxes.append(next_box)

                return

    def check_next_cell(point: Point, move: Direction) -> bool:
        if field[point] == "#":
            return False

        for box in boxes:
            if point in box.points:
                next_box = box + move

                if move == Direction.LEFT:
                    check = check_next_cell(next_box.points[0], move)
                elif move == Direction.RIGHT:
                    check = check_next_cell(next_box.points[1], move)
                else:
                    check = all(check_next_cell(next_point, move) for next_point in next_box.points)

                return check

        return True

    # print_state(boxes, field, robot)

    for move in moves:
        next_robot = robot + move

        if check_next_cell(next_robot, move):
            push(next_robot, move)
            robot = next_robot

    # print_state(boxes, field, robot)

    gps_sum = 0

    for box in boxes:
        box_gps = box.x + 100 * box.y

        gps_sum += box_gps

    print(gps_sum)


def print_state(boxes, field, robot):
    for y in range(field.height):
        for x in range(field.width):
            point = Point(x, y)

            if robot == point:
                print("@", end="")

                continue

            box_ = None

            for box in boxes:
                if point in box.points:
                    box_ = box

                    break

            if box_:
                print(box_[point], end="")

                continue

            print(field[x, y], end="")

        print()
    print()


if __name__ == '__main__':
    main()
