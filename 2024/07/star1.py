from pathlib import Path
from typing import List


def validate_equation(result: int, equation: List[int]) -> bool:
    if len(equation) == 0:
        return result == 0

    if result < 0:
        return False

    first, rest = equation[0], equation[1:]

    if result % first == 0:
        mul_result = validate_equation(result // first, rest)
    else:
        mul_result = False

    return mul_result or validate_equation(result - first, rest)


def main():
    result_sum = 0

    with Path("input.txt").open() as input_file:
        for line in input_file:
            line = line.strip()
            result, equation = line.split(": ", maxsplit=1)

            result = int(result)

            equation = [int(e) for e in equation.split()]
            equation.reverse()

            if validate_equation(result, equation):
                result_sum += result

            # print(line, validate_equation(result, equation))

    print(result_sum)


if __name__ == '__main__':
    main()
