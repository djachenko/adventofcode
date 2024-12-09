from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import List


def main():
    with Path("input.txt").open() as input_file:
        string = input_file.read()

    files = [int(c) for c in string]

    checksum = 0

    block_index = 0
    sector_index = 0
    rev_sector_index = len(files) - 1

    files_count = len(files)

    while sector_index < files_count:
        for i in range(files[sector_index]):
            block_value = sector_index / 2
            checksum += block_value * block_index
            block_index += 1

            print(int(block_value), end="")

        files[sector_index] = 0
        sector_index += 1

        if sector_index >= files_count:
            break

        for i in range(files[sector_index]):
            block_value = rev_sector_index / 2
            checksum += block_value * block_index
            block_index += 1

            print(int(block_value), end="")

            files[rev_sector_index] -= 1

            if files[rev_sector_index] == 0:
                rev_sector_index -= 1
                files[rev_sector_index] = 0
                rev_sector_index -= 1

        files[sector_index] = 0
        sector_index += 1

    print()
    print(int(checksum))


if __name__ == '__main__':
    main()
