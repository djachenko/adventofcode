from pathlib import Path


def main():
    result = 0

    with Path("input.txt").open() as input_file:
        for line in input_file:
            line = line.strip()

            digits = [c for c in line if c.isdigit()]

            calibration_value = int(digits[0] + digits[-1])

            result += calibration_value

    print(result)


if __name__ == '__main__':
    main()
