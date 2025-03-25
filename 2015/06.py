from itertools import product

from framework.aoc import *


def __run_instructions(field, commands):
    for line in INPUT.lines:
        command, start, _, end = line.rsplit(maxsplit=3)

        start_x, start_y = [int(s) for s in start.split(",")]
        end_x, end_y = [int(s) for s in end.split(",")]

        action = commands[command]

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                field[x, y] = action(field[x, y])


def star1() -> Output:
    field = {point: False for point in product(range(1000), repeat=2)}

    commands = {
        "turn on": lambda _: True,
        "turn off": lambda _: False,
        "toggle": lambda b: not b,
    }

    __run_instructions(field, commands)

    return len([value for value in field.values() if value])


def star2() -> Output:
    field = {point: 0 for point in product(range(1000), repeat=2)}

    commands = {
        "turn on": lambda p: p + 1,
        "turn off": lambda p: max(p - 1, 0),
        "toggle": lambda p: p + 2,
    }

    __run_instructions(field, commands)

    return sum(field.values())


if __name__ == '__main__':
    run(star1, star2)
