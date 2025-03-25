from itertools import permutations
from typing import Iterable, Tuple, List, Dict

from framework.aoc import *

Point = Tuple[str, str]


def __build_edges() -> Iterable[Tuple[Point, int]]:
    for line in INPUT.lines:
        words = line.strip(".").split()

        start = words[0]
        end = words[-1]

        weight = int(words[3])

        if words[2] == "lose":
            weight *= -1

        yield (start, end), weight


def __happiness(sitting: List[str], edges: Dict[Point, int]) -> int:
    total = 0

    for i in range(-1, len(sitting) - 1):
        left = sitting[i]
        right = sitting[i + 1]

        total += edges[left, right]
        total += edges[right, left]

    return total


def __count_total_happiness(edges: Dict[Point, int]) -> int:
    vertices = list({v for v, _ in edges})

    start_point = vertices[0]

    perms = permutations(vertices[1:])
    perms = [[start_point] + list(p) for p in perms]

    happinesses = [__happiness(perm, edges) for perm in perms]

    max_happiness = max(happinesses)

    return max_happiness


def star1() -> Output:
    return __count_total_happiness(dict(__build_edges()))


def star2() -> Output:
    edges = dict(__build_edges())
    vertices = {v for v, _ in edges}

    for vertex in vertices:
        edges["self", vertex] = 0
        edges[vertex, "self"] = 0

    return __count_total_happiness(edges)


if __name__ == '__main__':
    run(star1, star2)
