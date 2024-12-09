from collections import defaultdict
from pathlib import Path
from typing import Tuple, Dict, List

SIZE = 140
LEN = len("xmas")

Mapping = Dict[Tuple[int, int], str]


def convert_to_mappings(lines: List[str]) -> Mapping:
    mappings = defaultdict(lambda: "")

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            mappings[(x, y)] = char

    return mappings


def find_xmas(mappings: Mapping, dx: int, dy: int):
    count = 0

    for start_x in range(SIZE):
        for start_y in range(SIZE):
            string = ""

            for d in range(LEN):
                string += mappings[start_x + dx * d, start_y + dy * d]

            if string.lower() == "xmas":
                count += 1

    return count


def main():
    with Path("input.txt").open() as input_file:
        lines = [line for line in input_file]

    mappings = convert_to_mappings(lines)

    count = 0

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            count += find_xmas(mappings, dx, dy)

    print(count)


if __name__ == '__main__':
    main()
