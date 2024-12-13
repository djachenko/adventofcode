from pathlib import Path
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
    test_index = 0

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
        p = Point.from_tuple(get_x_y(prize_string, "="))

        p.x += 10000000000000
        p.y += 10000000000000

        i_top = (p.y * b.x - p.x * b.y)
        i_bottom = (a.y * b.x - b.y * a.x)

        i = 0
        j = 0

        if i_top % i_bottom == 0:
            i = i_top // i_bottom

            j_top = (p.x - a.x * i)

            if j_top % b.x == 0:
                j = j_top // b.x
            else:
                i = 0

        price = 3 * i + j

        total_price += price

    print(total_price)


if __name__ == '__main__':
    main()
