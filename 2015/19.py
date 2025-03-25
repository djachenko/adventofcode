from framework.aoc import *
from utils.funcs import find_all

REPLACEMENTS = list(tuple(line.split(" => ")) for line in INPUT.blocks[0])
MOLECULE = INPUT.blocks[1][0]


def star1() -> Output:
    results = set()

    for src, dst in REPLACEMENTS:
        splits = MOLECULE.split(src)

        results |= {src.join(splits[:r + 1]) + dst + src.join(splits[r + 1:]) for r in range(len(splits) - 1)}

    return len(results)


ELECTRON = "e"


def star2():
    reverse_replacements = list((dst, src) for src, dst in REPLACEMENTS)

    steps_count = 0
    string = MOLECULE

    while True:
        if string == ELECTRON:
            break

        for src, dst in reverse_replacements:
            replace_count = len(find_all(string, src))
            new_string = string.replace(src, dst)

            steps_count += replace_count

            string = new_string

    return steps_count


if __name__ == '__main__':
    run(star1, star2)
