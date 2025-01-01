from pathlib import Path


def main():
    left_list = []
    right_list = []

    with Path("input.txt").open() as input_file:
        for line in input_file:
            a, b = (int(s) for s in line.split())

            left_list.append(a)
            right_list.append(b)

    left_list.sort()
    right_list.sort()

    diffs = [abs(x - y) for x, y in zip(left_list, right_list)]

    result = sum(diffs)

    print(result)


if __name__ == '__main__':
    main()
