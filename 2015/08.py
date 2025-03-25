from framework.aoc import *


def star1() -> Output:
    total = 0

    for line in INPUT.lines:
        decoded = line.encode('utf-8').decode('unicode-escape')

        diff = len(line) - len(decoded) + 2

        total += diff

    return total


def star2() -> Output:
    total = 0

    symbols_to_escape = [
        "\"",
        "\\",
    ]

    for line in INPUT.lines:
        diff = 2

        for c in line:
            if c in symbols_to_escape:
                diff += 1

        total += diff

    return total


if __name__ == '__main__':
    run(star1, star2)
