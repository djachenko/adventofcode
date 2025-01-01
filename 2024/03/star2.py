import re
from pathlib import Path


def main():
    with Path("input.txt").open() as input_file:
        program = ""

        for line in input_file:
            program += line

    result = []

    for subprogram in program.split("do()"):
        enabled = subprogram.split("don't()")[0]

        result += re.findall(r"mul\((\d+),(\d+)\)", enabled)

    total_sum = 0

    for a, b in result:
        total_sum += int(a) * int(b)

    print(total_sum)


if __name__ == '__main__':
    main()
