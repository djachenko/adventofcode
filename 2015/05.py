import string

from framework.aoc import *

VOWELS = "aeiou"

DISALLOWED_SUBSTRINGS = [
    "ab",
    "cd",
    "pq",
    "xy",
]

DOUBLE_LETTERS = [c * 2 for c in string.ascii_lowercase]


def star1() -> Output:
    count = 0

    for line in INPUT.lines:
        if len([c for c in line if c in VOWELS]) < 3:
            continue

        if any(s in line for s in DISALLOWED_SUBSTRINGS):
            continue

        if not any(s in line for s in DOUBLE_LETTERS):
            continue

        count += 1

    return count


def star2() -> Output:
    count = 0

    for line in INPUT.lines:
        rule1 = False
        rule2 = False

        for i in range(len(line) - 2):
            if line[i: i + 2] in line[i + 2:]:
                rule1 = True

            if line[i] == line[i + 2]:
                rule2 = True

            if rule1 and rule2:
                count += 1

                break

    return count


if __name__ == '__main__':
    run(star1, star2)
