from collections import defaultdict
from pathlib import Path


def main():
    left_list = []
    right_list = []

    with Path("input.txt").open() as input_file:
        for line in input_file:
            a, b = (int(s) for s in line.split())

            left_list.append(a)
            right_list.append(b)

    right_stats = defaultdict(lambda: 0)

    for item in right_list:
        right_stats[item] += 1

    similarity_score = sum(left * right_stats[left] for left in left_list)

    print(similarity_score)


if __name__ == '__main__':
    main()
