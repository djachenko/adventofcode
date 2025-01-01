from itertools import combinations

from utils import read_by_line


def main():
    edges = set()
    vertices = set()

    for line in read_by_line():
        start, end = line.split("-")

        edges.add((start, end))
        edges.add((end, start))

        vertices.add(start)
        vertices.add(end)

    combs = combinations(vertices, 3)

    count = 0

    for comb in combs:
        if not any(pc.startswith("t") for pc in comb):
            continue

        connections = list(combinations(comb, 2))

        if not all(connection in edges for connection in connections):
            continue

        count += 1

    print(count)


if __name__ == '__main__':
    main()
