from framework.aoc import *

SEPARATOR = "x"

dimensions = []

for line in INPUT.lines:
    dimensions.append([int(i) for i in line.split(SEPARATOR)])


def star1() -> Output:
    total = 0

    for w, l, h in dimensions:
        side1 = l * w
        side2 = w * h
        side3 = h * l

        square = 2 * (side1 + side2 + side3) + min(side1, side2, side3)

        total += square

    return total


def star2() -> Output:
    total = 0

    for w, l, h in dimensions:
        smallest_perimeter = 2 * (w + l + h - max(w, l, h))
        volume = w * l * h

        ribbon = volume + smallest_perimeter

        total += ribbon

    return total


if __name__ == '__main__':
    run(star1, star2)
