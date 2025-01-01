from math import log10
from pathlib import Path


def split_int(a: int) -> (int, int):
    length = length_of_int(a)

    splitter = pow(10, length / 2)

    return int(a / splitter), int(a % splitter)


def length_of_int(a: int) -> int:
    if a == 0:
        return 1

    return int(log10(a)) + 1


cache = {}


def count(stone: int, depth: int) -> int:
    if depth == 0:
        return 1

    if (stone, depth) in cache:
        return cache[stone, depth]

    length_of_stone = length_of_int(stone)

    if stone == 0:
        result = count(1, depth - 1)
    elif length_of_stone % 2 == 0:
        a, b = split_int(stone)

        result = count(a, depth - 1) + count(b, depth - 1)
    else:
        result = count(stone * 2024, depth - 1)

    cache[stone, depth] = result

    return result


def main():
    with Path("input.txt").open() as input_file:
        string = input_file.read()

    stones = [int(c) for c in string.split()]

    blink_count = 75
    total_sum = 0

    for stone in stones:
        total_sum += count(stone, depth=blink_count)

    print(total_sum)


if __name__ == '__main__':
    main()
