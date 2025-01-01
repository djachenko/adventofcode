from collections import defaultdict

from utils import read_by_line


def bron_kerbosch(R, P, X, neighbour_sets):
    if not P and not X:
        return [R]

    result = []

    for v in P.copy():
        result += bron_kerbosch(
            R | {v},
            P & neighbour_sets[v],
            X & neighbour_sets[v],
            neighbour_sets,
        )

        P.remove(v)
        X.add(v)

    return result


def main():
    edges = set()

    for line in read_by_line():
        start, end = line.split("-")

        edges.add((start, end))
        edges.add((end, start))

    neighbour_sets = defaultdict(set)

    for src, dest in edges:
        neighbour_sets[src].add(dest)

    cliques = bron_kerbosch(
        R=set(),
        P=set(neighbour_sets.keys()),
        X=set(),
        neighbour_sets=neighbour_sets,
    )

    cliques.sort(key=lambda x: len(x), reverse=True)

    largest_clique = list(cliques[0])
    largest_clique.sort()

    print(','.join(largest_clique))



if __name__ == '__main__':
    main()
