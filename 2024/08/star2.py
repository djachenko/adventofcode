from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from pathlib import Path


@dataclass
class Node:
    x: int
    y: int


def main():
    field_width = 0
    field_height = 0

    nodes_mapping = defaultdict(lambda: [])
    field = {}

    with Path("input.txt").open() as input_file:
        for y, line in enumerate(input_file):
            line = line.strip()

            field_width = len(line)
            field_height = y + 1

            for x, cell in enumerate(line):
                if cell.isalnum():
                    nodes_mapping[cell].append(Node(x, y))

                field[x, y] = cell

    def is_valid(node: Node) -> bool:
        return node.x in range(field_width) and node.y in range(field_height)

    antinodes = []

    for frequency in nodes_mapping:
        locations = nodes_mapping[frequency]

        pairs = product(locations, locations)
        pairs = list(pairs)

        for node1, node2 in pairs:
            if node1 is node2:
                continue

            dx = node2.x - node1.x
            dy = node2.y - node1.y

            step = 0

            while True:
                step += 1

                antinode = Node(
                    x=node1.x + dx * step,
                    y=node1.y + dy * step
                )

                if is_valid(antinode):
                    antinodes.append(antinode)
                else:
                    break

    antinodes = [(antinode.x, antinode.y) for antinode in antinodes]
    antinodes = list(set(antinodes))

    print(len(antinodes))


if __name__ == '__main__':
    main()
