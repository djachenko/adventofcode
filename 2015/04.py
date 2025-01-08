from hashlib import md5

from framework.aoc import *


def __main(prefix_len: int) -> int:
    i = 1
    prefix = "0" * prefix_len

    while True:
        string = INPUT.line + str(i)

        md5_hash = md5(string.encode("utf-8")).hexdigest()

        if md5_hash.startswith(prefix):
            return i

        i += 1


def star1() -> Output:
    return __main(5)


def star2() -> Output:
    return __main(6)


if __name__ == '__main__':
    run(star1, star2)
