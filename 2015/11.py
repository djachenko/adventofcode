from string import ascii_lowercase

from framework.aoc import *
from utils.funcs import count_if


def __next_password(password: str) -> str:
    result = list(password)

    for i in reversed(range(-len(password), 0)):
        if password[i] == "z":
            result[i] = "a"
        else:
            index = ascii_lowercase.index(password[i])

            result[i] = ascii_lowercase[index + 1]

            break

    return "".join(result)


__STRAIGHTS = [ascii_lowercase[i: i + 3] for i in range(len(ascii_lowercase) - 2)]
__FORBIDDEN_LETTERS = ["i", "o", "l", ]
__DOUBLES = [c + c for c in ascii_lowercase]


def __is_valid(password: str) -> bool:
    return any(straight in password for straight in __STRAIGHTS) and \
        not any(letter in password for letter in __FORBIDDEN_LETTERS) and \
        count_if(__DOUBLES, lambda d: d in password) == 2


def __next_valid_password(expired_password: str) -> str:
    password = __next_password(expired_password)

    while not __is_valid(password):
        password = __next_password(password)

    return password


@lru_cache()
def star1() -> Output:
    return __next_valid_password(INPUT.line)


def star2() -> Output:
    return __next_valid_password(star1())


if __name__ == '__main__':
    run(star1, star2)
