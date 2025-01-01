from dataclasses import dataclass
from typing import List

from utils import read_by_line, Field, Point, first, Direction

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
            for neighbour in point.neighbours:
                if neighbour in new_points or neighbour in region:
                    continue

                if field[neighbour] == region_value:
                    new_points.append(neighbour)

        if not new_points:
            break
        else:
            region += new_points

    return region


@dataclass
class Fence:
    point: Point
    direction: Direction

    @property
    def x(self) -> int:
        return self.point.x

    @property
    def y(self) -> int:
        return self.point.y

    @property
    def neighbours(self) -> List['Fence']:
        if self.direction.dx == 0:
            return [
                Fence(Point(self.point.x - 1, self.point.y), self.direction),
                Fence(Point(self.point.x + 1, self.point.y), self.direction),
            ]
        else:
            return [
                Fence(Point(self.point.x, self.point.y - 1), self.direction),
                Fence(Point(self.point.x, self.point.y + 1), self.direction),
            ]


def find_fence(field: Field, region: List[Point]) -> List[Fence]:
    if not region:
        return []

    fence_cells = []
    region_value = field[region[0]]

    for point in region:
        for direction in Direction:
            neighbour = point + direction

            if field[neighbour] != region_value:
                fence_cells.append(Fence(
                    point=point,
                    direction=direction
                ))

    return fence_cells


def split_into_walls(fence: List[Fence]) -> List[List[Fence]]:
    fence_original = fence

    fence = fence.copy()
    walls = []

    while fence:
        wall = [fence[0]]

        while True:
            new_fences = []

            for cell in wall:
                for neighbour in cell.neighbours:
                    if neighbour in new_fences or neighbour in wall:
                        continue

                    if neighbour not in fence:
                        continue

                    new_fences.append(neighbour)

            if not new_fences:
                break
            else:
                wall += new_fences

        walls.append(wall)

        for cell in wall:
            fence.remove(cell)

    assert len(fence_original) == sum(len(wall) for wall in walls)

    return walls


def main():
    field = Field.read(read_by_line(), default_factory=lambda: EMPTY)

    total_price = 0

    while True:
        non_empty = get_first_nonempty(field)

        if non_empty is None:
            break

        region = find_region(field, non_empty)
        fence = find_fence(field, region)
        walls = split_into_walls(fence)

        area = len(region)
        sides_count = len(walls)

        region_price = area * sides_count

        total_price += region_price

        for point in region:
            field[point] = EMPTY

    print(total_price)


if __name__ == '__main__':
    main()
