from collections import defaultdict
from dataclasses import dataclass
from importlib.metadata import files
from itertools import product
from pathlib import Path
from typing import List


def main():
    with Path("input.txt").open() as input_file:
        string = input_file.read()

    files = [int(c) for c in string]

    for i in range(len(files)):
        if i % 2 == 0:
            files[i] *= -1

    def is_file(item: int) -> bool:
        return item < 0

    checksum = 0

    block_index = 0
    for sector_index in range(len(files)):
        sector = files[sector_index]

        if is_file(sector):
            sector *= -1

            for i in range(sector):
                block_value = sector_index / 2
                checksum += block_value * block_index
                block_index += 1

                print(int(block_value), end="")
        else:
            rev_sector_index = len(files) - 1

            while sector > 0 and rev_sector_index > sector_index:
                if not is_file(files[rev_sector_index]):
                    rev_sector_index -= 2
                    continue

                rev_file = files[rev_sector_index]

                rev_file *= -1

                if rev_file <= sector:

                    for i in range(rev_file):
                        block_value = rev_sector_index / 2
                        checksum += block_value * block_index
                        block_index += 1

                        print(int(block_value), end="")

                    sector -= rev_file
                    files[rev_sector_index] *= -1

                rev_sector_index -= 2

            files[sector_index] = sector

            block_index += sector

    print(int(checksum))


if __name__ == '__main__':
    main()
