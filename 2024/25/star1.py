from itertools import product

from utils import INPUT

WIDTH = 5
HEIGHT = 7

FILLED_CELL = "#"
FILLED_ROW = FILLED_CELL * WIDTH


def main():
    schemes = INPUT.blocks

    keys = []
    locks = []

    for scheme in schemes:
        heights = [0 for _ in range(WIDTH)]

        for row in scheme:
            for i, cell in enumerate(row):
                if cell == FILLED_CELL:
                    heights[i] += 1

        if scheme[0] == FILLED_ROW:
            locks.append(heights)
        elif scheme[-1] == FILLED_ROW:
            keys.append(heights)
        else:
            assert False

    count = 0

    for key, lock in product(keys, locks):

        if all(k + l <= HEIGHT for k, l in zip(key, lock)):
            count += 1

    print(count)


if __name__ == '__main__':
    main()
