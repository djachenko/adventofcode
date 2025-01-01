from utils import read_by_line


def main():
    stream = read_by_line()

    towels_string: str = next(stream)

    towels = towels_string.split(", ")

    next(stream)

    designs = [line for line in stream]

    count = 0

    def is_valid(design: str) -> bool:
        if not design:
            return True

        for towel in towels:
            if not design.startswith(towel):
                continue

            if is_valid(design[len(towel):]):
                return True

        return False

    for design in designs:
        if is_valid(design):
            count += 1

    print(count)


if __name__ == '__main__':
    main()
