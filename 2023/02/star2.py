from collections import defaultdict
from pathlib import Path


def main():
    result = 0

    with Path("input.txt").open() as input_file:
        for i, line in enumerate(input_file):
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

    print(result)


if __name__ == '__main__':
    main()
