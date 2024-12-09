from collections import defaultdict
from pathlib import Path
from typing import Tuple, Dict, List

SIZE = 140

Mapping = Dict[Tuple[int, int], str]


def convert_to_mappings(lines: List[str]) -> Mapping:
    mappings = defaultdict(lambda: "")

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            mappings[(x, y)] = char

    return mappings


def check_line(xmas: Mapping, start_x: int, start_y: int, dx: int, dy: int) -> bool:
    line = ""

    for d in range(3):
        line += xmas[start_x + dx * d, start_y + dy * d]

    return line.lower() == "mas"


def check_xmas(xmas: Mapping) -> bool:
    return all([
        check_line(xmas, start_x=0, start_y=0, dx=1, dy=1),
        check_line(xmas, start_x=0, start_y=2, dx=1, dy=-1),
    ]) or all([
        check_line(xmas, start_x=2, start_y=0, dx=-1, dy=1),
        check_line(xmas, start_x=2, start_y=2, dx=-1, dy=-1),
    ]) or all([
        check_line(xmas, start_x=2, start_y=0, dx=-1, dy=1),
        check_line(xmas, start_x=0, start_y=0, dx=1, dy=1),
    ]) or all([
        check_line(xmas, start_x=2, start_y=2, dx=-1, dy=-1),
        check_line(xmas, start_x=0, start_y=2, dx=1, dy=-1),
    ])


def count_xmases(mapping: Mapping):
    count = 0

    for start_x in range(SIZE):
        for start_y in range(SIZE):
            cross_mapping = defaultdict(lambda: "")

            for x in range(3):
                for y in range(3):
                    cross_mapping[x, y] = mapping[start_x + x, start_y + y]

            if check_xmas(cross_mapping):
                count += 1

    return count


def main():
    with Path("input.txt").open() as input_file:
        lines = [line for line in input_file]

    mapping = convert_to_mappings(lines)

    total_sum = count_xmases(mapping)

    print(total_sum)


if __name__ == '__main__':
    main()
