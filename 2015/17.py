from itertools import combinations

from framework.aoc import *

containers = [int(line) for line in INPUT.lines]

VOLUME = 150


def star1() -> Output:
    count = 0

    for length in range(len(containers)):
        for combination in combinations(containers, length):
            if sum(combination) == VOLUME:
                count += 1

    return count


def star2() -> Output:
    for length in range(len(containers)):
        count = 0

        for combination in combinations(containers, length):
            if sum(combination) == VOLUME:
                count += 1

        if count > 0:
            return count


if __name__ == '__main__':
    run(star1, star2)
