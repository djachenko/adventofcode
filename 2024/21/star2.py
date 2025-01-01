from functools import lru_cache
from itertools import product
from typing import Dict, List

from utils import Point, Direction, INPUT

FORBIDDEN = " "

NUMERIC_KEYPAD = {
    (0, 0): "7",
    (1, 0): "8",
    (2, 0): "9",
    (0, 1): "4",
    (1, 1): "5",
    (2, 1): "6",
    (0, 2): "1",
    (1, 2): "2",
    (2, 2): "3",
    (0, 3): FORBIDDEN,
    (1, 3): "0",
    (2, 3): "A",
}

NUMERIC_KEYPAD = {char: point for point, char in NUMERIC_KEYPAD.items()}
NUMERIC_KEYPAD = {char: Point.from_tuple(point) for char, point in NUMERIC_KEYPAD.items()}

DIRECTIONAL_KEYPAD = {
    (0, 0): FORBIDDEN,
    (1, 0): "^",
    (2, 0): "A",
    (0, 1): "<",
    (1, 1): "V",
    (2, 1): ">",
}

DIRECTIONAL_KEYPAD = {char: point for point, char in DIRECTIONAL_KEYPAD.items()}
DIRECTIONAL_KEYPAD = {char: Point.from_tuple(point) for char, point in DIRECTIONAL_KEYPAD.items()}


def sign(x: int) -> int:
    if x < 0:
        return -1

    return 1


def complexity(code: str, sequence_price: int) -> int:
    int_code = int(code[:-1])

    return sequence_price * int_code


def build_paths(path: List[Direction], diff: Point) -> List[List[Direction]]:
    if not diff:
        return [path]

    result = []

    if diff.x != 0:
        x_sign = sign(diff.x)
        x_direction = Direction.from_dx_dy(x_sign, 0)

        result += build_paths(path + [x_direction], diff - x_direction)

    if diff.y != 0:
        y_sign = sign(diff.y)
        y_direction = Direction.from_dx_dy(0, y_sign)

        result += build_paths(path + [y_direction], diff - y_direction)

    return result


Keypad = Dict[str, Point]


def is_valid(path: List[Direction], keypad: Keypad, start: Point) -> bool:
    check_point = start
    forbidden_point = keypad[FORBIDDEN]

    for direction in path:
        check_point += direction

        if forbidden_point == check_point:
            return False

    return True


def path_to_string(path: List[Direction]) -> str:
    return "".join(str(direction) for direction in path)


def build_sequences(keypad: Keypad, start: str, end: str) -> List[str]:
    start_point = keypad[start]
    end_point = keypad[end]

    diff = end_point - start_point

    direction_paths = build_paths([], diff)
    direction_paths = [path for path in direction_paths if is_valid(path, keypad, start_point)]

    strings = [path_to_string(path) + "A" for path in direction_paths]

    return strings


def filter_shortest(strings: List[str]) -> List[str]:
    if not strings:
        return []

    result = []
    min_length = len(strings[0])

    for string in strings:
        current_length = len(string)

        if current_length < min_length:
            result = []
            min_length = current_length

        if current_length == min_length:
            result.append(string)

    return result


def price_of_sequence(sequence, depth):
    start = "A"

    sequence_sum = 0

    for char in sequence:
        pair_sum = price_between_chars(start, char, depth - 1)

        sequence_sum += pair_sum

        start = char

    return sequence_sum


@lru_cache(maxsize=None)
def price_between_chars(start: str, end: str, depth: int) -> int:
    if depth == 0:
        return 1

    keypad = DIRECTIONAL_KEYPAD

    sequences = build_sequences(keypad, start, end)
    min_length = None

    for sequence in sequences:
        sequence_sum = price_of_sequence(sequence, depth)

        if min_length is None:
            min_length = sequence_sum
        else:
            min_length = min(min_length, sequence_sum)

    return min_length


def main():
    codes = INPUT.lines

    total_sum = 0

    for code in codes:
        keypad = NUMERIC_KEYPAD

        output_sequences = []
        start = "A"

        subsequences = []

        for char in code:
            sequences = build_sequences(keypad, start, char)

            subsequences.append(sequences)

            start = char

        sequences_combinations = list(product(*subsequences))

        output_sequences += ["".join(comb) for comb in sequences_combinations]

        output_sequences = filter_shortest(output_sequences)

        prices = [price_of_sequence(sequence, 26) for sequence in output_sequences]

        min_price = min(prices)

        code_complexity = complexity(code, min_price)
        total_sum += code_complexity

    print(total_sum)


if __name__ == '__main__':
    main()
