from math import ceil, sqrt
from typing import List

from framework.aoc import *

PRESENTS_COUNT = int(INPUT.line)


def __get_dividers(x: int) -> List[int]:
    result = []

    for divider in range(1, ceil(sqrt(x)) + 1):
        if x % divider == 0:
            result.append(divider)

    for divider in reversed(result):
        y = x // divider
        result.append(y)

    result = sorted(list(set(result)))

    return result


def __get_good_dividers(x: int) -> List[int]:
    result = []

    for divider in range(1, ceil(sqrt(x)) + 1):
        if x % divider == 0:
            result.append(divider)

    for divider in reversed(result):
        y = x // divider
        result.append(y)

    result = [d for d in result if x // d <= 50]

    result = sorted(list(set(result)))

    return result


def star1() -> Output:
    house = 1

    while True:
        if sum(__get_dividers(house)) * 10 > PRESENTS_COUNT:
            return house
        else:
            house += 1


def star2() -> Output:
    house = 1

    while True:
        if sum(__get_good_dividers(house)) * 11 > PRESENTS_COUNT:
            return house
        else:
            house += 1


if __name__ == '__main__':
    run(star1, star2)
