from typing import List

from framework.aoc import *


def __build_edges():
    for line in INPUT.lines:
        start, _, end, _, distance = line.split()

        distance = int(distance)

        yield (start, end), distance
        yield (end, start), distance


edges = dict(__build_edges())
vertices = {a for a, _ in edges}

MAX_DISTANCE = sum(edges.values()) + 1


def __find_shortest_path(path: List[str], distance: int) -> int:
    if len(path) == len(vertices):
        return distance

    last = path[-1]
    min_distance = MAX_DISTANCE

    for vertex in vertices:
        if vertex in path:
            continue

        min_distance = min(min_distance, __find_shortest_path(path + [vertex], distance + edges[last, vertex]))

    return min_distance


def __find_longest_path(path: List[str], distance: int) -> int:
    if len(path) == len(vertices):
        return distance

    last = path[-1]
    max_distance = -1

    for vertex in vertices:
        if vertex in path:
            continue

        max_distance = max(max_distance, __find_longest_path(path + [vertex], distance + edges[last, vertex]))

    return max_distance


def star1() -> Output:
    return min(__find_shortest_path([vertex], 0) for vertex in vertices)


def star2() -> Output:
    return max(__find_longest_path([vertex], 0) for vertex in vertices)


if __name__ == '__main__':
    run(star1, star2)
