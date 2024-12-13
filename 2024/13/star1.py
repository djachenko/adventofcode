from typing import List, Tuple

from utils import read_by_line, Point


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    lines = list(read_by_line())

    lines = [line for line in lines if line]

    games: List[List[str]] = list(chunks(lines, 3))

    total_price = 0

    for a_string, b_string, prize_string in games:
        a_string: str
        b_string: str
        prize_string: str

        def get_x_y(string: str, sep: str) -> Tuple[int, int]:
            string = string.split(": ")[1]
            x_string, y_string = string.split(", ")

            x = x_string.split(sep)[1]
            y = y_string.split(sep)[1]

            x = int(x)
            y = int(y)

            return x, y

        a = Point.from_tuple(get_x_y(a_string, "+"))
        b = Point.from_tuple(get_x_y(b_string, "+"))
        prize = Point.from_tuple(get_x_y(prize_string, "="))

        result = (0, 0)

        for j in range(100):
            for i in range(100):
                if a.x * i + b.x * j == prize.x and a.y * i + b.y * j == prize.y:
                    result = (i, j)

        i, j = result

        price = 3 * i + j

        total_price += price

    print(total_price)


if __name__ == '__main__':
    main()
