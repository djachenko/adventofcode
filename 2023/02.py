from collections import defaultdict

from framework.aoc import *


def star1() -> Output:
    color_counts = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    result = 0

    for i, line in enumerate(INPUT.lines):
        line = line.strip()
        _, line = line.split(": ")

        good_game = True

        for grab in line.split("; "):
            for cube in grab.split(","):
                count, color = cube.split()
                count = int(count)

                if count > color_counts[color]:
                    good_game = False

        if good_game:
            result += i + 1

    return result


def star2() -> Output:
    result = 0

    for i, line in enumerate(INPUT.lines):
        line = line.strip()
        _, line = line.split(": ")

        cube_counts = defaultdict(lambda: 0)

        for grab in line.split("; "):
            for cube in grab.split(","):
                count, color = cube.split()
                count = int(count)

                cube_counts[color] = max(cube_counts[color], count)

        power = 1

        for count in cube_counts.values():
            power *= count

        result += power

    return result


if __name__ == '__main__':
    run(star1, star2)
