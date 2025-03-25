from typing import List

from framework.aoc import *

Report = List[int]


def __build_diffs(report: Report) -> Report:
    a = report[1:]
    b = report[:-1]

    result = [x - y for x, y in zip(a, b)]

    return result


def __is_increasing(diffs: Report) -> bool:
    return all(diff >= 0 for diff in diffs)


def __is_decreasing(diffs: Report) -> bool:
    return all(diff <= 0 for diff in diffs)


def __is_valid(diffs: Report) -> bool:
    valid_range = range(1, 4)

    return all(abs(diff) in valid_range for diff in diffs)


def __is_safe(report: Report) -> bool:
    diffs = __build_diffs(report)

    return __is_valid(diffs) and (__is_increasing(diffs) or __is_decreasing(diffs))


REPORTS = [[int(num) for num in line.split()] for line in INPUT.lines]


def star1() -> Output:
    count = 0

    for report in REPORTS:
        if __is_safe(report):
            count += 1

            continue

    return count


def star2() -> Output:
    count = 0

    for report in REPORTS:
        if __is_safe(report):
            count += 1

            continue

        for i in range(len(report)):
            modified_report = report.copy()
            modified_report.pop(i)

            if __is_safe(modified_report):
                count += 1

                break

    return count


if __name__ == '__main__':
    run(star1, star2)
