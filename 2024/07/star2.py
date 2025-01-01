from collections import defaultdict
from pathlib import Path
from typing import List


def validate_equation(result: int, equation: List[int]) -> bool:
    def plus(a, b):
        return a + b

    def star(a, b):
        return a * b

    def concat(a, b):
        return int(f"{a}{b}")

    first = equation[0]

    if len(equation) == 1:
        return first == result

    second = equation[1]
    rest = equation[2:]

    return validate_equation(result, [plus(first, second)] + rest) or \
        validate_equation(result, [star(first, second)] + rest) or \
        validate_equation(result, [concat(first, second)] + rest)


def main():
    result_sum = 0

    with Path("input.txt").open() as input_file:
        for line in input_file:
            line = line.strip()
            result, equation = line.split(": ", maxsplit=1)

            result = int(result)

            equation = [int(e) for e in equation.split()]

            if validate_equation(result, equation):
                result_sum += result

    print(result_sum)


if __name__ == '__main__':
    main()
