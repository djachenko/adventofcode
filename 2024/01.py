from collections import defaultdict

from framework.aoc import *

left_list = []
right_list = []

for line in INPUT.lines:
    a, b = (int(s) for s in line.split())

    left_list.append(a)
    right_list.append(b)


def star1() -> Output:
    left_list.sort()
    right_list.sort()

    diffs = [abs(x - y) for x, y in zip(left_list, right_list)]

    result = sum(diffs)

    return result


def star2() -> Output:
    right_stats = defaultdict(lambda: 0)

    for item in right_list:
        right_stats[item] += 1

    similarity_score = sum(left * right_stats[left] for left in left_list)

    return similarity_score


if __name__ == '__main__':
    run(star1, star2)
