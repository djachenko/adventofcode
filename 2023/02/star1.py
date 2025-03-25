from pathlib import Path

COLOR_COUNTS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def main():
    result = 0

    with Path("input.txt").open() as input_file:
        for i, line in enumerate(input_file):
            line = line.strip()
            _, line = line.split(": ")

            good_game = True

            for grab in line.split("; "):
                for cube in grab.split(","):
                    count, color = cube.split()
                    count = int(count)

                    if count > COLOR_COUNTS[color]:
                        good_game = False

            if good_game:
                result += i + 1

    print(result)


if __name__ == '__main__':
    main()
