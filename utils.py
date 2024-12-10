from pathlib import Path
from typing import Tuple


class Field:
    @property
    def height(self):
        if not self.field:
            return 0

        return max(y for _, y in self.field) + 1

    @property
    def width(self):
        if not self.field:
            return 0

        return max(x for x, _ in self.field) + 1

    def __init__(self, default_factory=lambda: None):
        self.field = {}
        self.factory = default_factory

    def __getitem__(self, coordinate: Tuple[int, int]):
        x, y = coordinate

        if x not in range(self.width) or y not in range(self.height):
            return self.factory()

        return self.field[x, y]

    def __setitem__(self, coordinate: Tuple[int, int], value):
        x, y = coordinate

        self.field[x, y] = value

    def __iter__(self):
        return iter(self.field)

    @staticmethod
    def read(path: Path, default_factory=lambda: None, converter=lambda x: x) -> 'Field':
        field = Field(default_factory)

        with path.open() as input_file:
            for y, line in enumerate(input_file):
                line = line.strip()

                for x, cell in enumerate(line):
                    field[x, y] = converter(cell)

        return field
