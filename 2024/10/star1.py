from pathlib import Path
from typing import List, Tuple

from utils import Field


def count_tops(field: Field, x: int, y: int, step: int) -> List[Tuple[int, int]]:
    current_cell = field[x, y]

    if current_cell is None:
        return []

    if current_cell != step:
        return []

    if current_cell == 9:
        return [(x, y)]

    next_step = current_cell + 1

    return count_tops(field, x + 1, y, next_step) + \
        count_tops(field, x - 1, y, next_step) + \
        count_tops(field, x, y + 1, next_step) + \
        count_tops(field, x, y - 1, next_step)


def main():
    path = Path("input.txt")
    field = Field.read(path, converter=int)

    trail_ends = []

    for x, y in field:
        if field[x, y] == 0:
            trail_ends += list(set(count_tops(field, x, y, 0)))

    print(len(trail_ends))


if __name__ == '__main__':
    main()
