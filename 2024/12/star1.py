from typing import List

from utils import read_by_line, Field, Point, first

EMPTY = " "


def get_first_nonempty(field: Field) -> Point | None:
    r = first(field, lambda t: field[t] != EMPTY)

    if r:
        return Point.from_tuple(r)

    return None


def find_region(field: Field, non_empty: Point) -> List[Point]:
    region = [non_empty]
    region_value = field[non_empty]

    while True:
        new_points = []

        for point in region:
            for neighbour in point.neighbours():
                if neighbour in new_points or neighbour in region:
                    continue

                if field[neighbour] == region_value:
                    new_points.append(neighbour)

        if not new_points:
            break
        else:
            region += new_points

    return region


def find_fence(field: Field, region: List[Point]) -> List[Point]:
    if not region:
        return []

    fence_cells = []
    region_value = field[region[0]]

    for point in region:
        for neighbour in point.neighbours():
            if field[neighbour] != region_value:
                fence_cells.append(neighbour)

    return fence_cells


def main():
    field = Field.read(read_by_line(), default_factory=lambda: EMPTY)

    total_price = 0

    while True:
        non_empty = get_first_nonempty(field)

        if non_empty is None:
            break

        region = find_region(field, non_empty)
        fence = find_fence(field, region)

        area = len(region)
        perimeter = len(fence)

        region_price = area * perimeter

        total_price += region_price

        region_value = field[non_empty]
        print(f"{region_value}: {region_price}")

        for point in region:
            field[point] = EMPTY

    print(total_price)


if __name__ == '__main__':
    main()
