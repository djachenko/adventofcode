from framework.aoc import *


def __look_and_say(repeat_count: int) -> int:
    sequence = INPUT.line

    for _ in range(repeat_count):
        count = 0
        pattern = " "

        result = ""

        for c in sequence:
            if c != pattern:
                result += f"{count}{pattern}"

                pattern = c
                count = 1
            else:
                count += 1

        result += f"{count}{pattern}"
        result = result[2:]

        sequence = result

    return len(sequence)


def star1() -> Output:
    return __look_and_say(40)


def star2() -> Output:
    return __look_and_say(50)


if __name__ == '__main__':
    run(star1, star2)
