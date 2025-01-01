from framework.aoc import *

string = INPUT.line


def star1() -> Output:
    result = 0

    for c in string:
        if c == "(":
            result += 1
        elif c == ")":
            result -= 1

    return result


def star2() -> Output:
    result = 0

    for i, c in enumerate(string):
        if c == "(":
            result += 1
        elif c == ")":
            result -= 1

        if result < 0:
            return i + 1


if __name__ == '__main__':
    run(star1, star2)
