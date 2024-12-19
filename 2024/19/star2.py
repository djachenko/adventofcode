from functools import lru_cache

from utils import read_by_line


def main():
    stream = read_by_line()

    towels_string: str = next(stream)

    towels = towels_string.split(", ")

    next(stream)

    designs = [line for line in stream]

    @lru_cache(maxsize=None)
    def is_valid(design: str) -> int:
        if not design:
            return 1

        count = 0

        for towel in towels:
            if not design.startswith(towel):
                continue

            count += is_valid(design[len(towel):])

        return count

    count = 0

    for design in designs:
        count += is_valid(design)

    print(count)


if __name__ == '__main__':
    main()
