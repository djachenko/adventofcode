from framework.aoc import *


def __parse_sue(line: str):
    name, properties = line.split(": ", maxsplit=1)

    properties = properties.split(", ")
    properties = [p.split(": ") for p in properties]

    properties = {n: int(a) for n, a in properties}

    return properties


sues = [__parse_sue(line) for line in INPUT.lines]

pattern_sue = __parse_sue("Sue 0: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, goldfish: "
                        "5, trees: 3, cars: 2, perfumes: 1")


def star1() -> Output:
    for i, sue in enumerate(sues):
        valid = True

        for key in sue:
            if sue[key] != pattern_sue[key]:
                valid = False

                break

        if valid:
            return i + 1

    return None


def star2() -> Output:
    comparators = {
        "children": lambda a, b: a == b,
        "samoyeds": lambda a, b: a == b,
        "akitas": lambda a, b: a == b,
        "vizslas": lambda a, b: a == b,
        "cars": lambda a, b: a == b,
        "perfumes": lambda a, b: a == b,

        "cats": lambda a, b: a > b,
        "trees": lambda a, b: a > b,

        "pomeranians": lambda a, b: a < b,
        "goldfish": lambda a, b: a < b,
    }

    for i, sue in enumerate(sues):
        valid = True

        for key in sue:
            if not comparators[key](sue[key], pattern_sue[key]):
                valid = False

                break

        if valid:
            return i + 1

    return None


if __name__ == '__main__':
    run(star1, star2)
