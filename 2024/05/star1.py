from pathlib import Path
from typing import Tuple, List


def validate(update: List[int], rules: List[Tuple[int, int]]) -> bool:
    for i, page in enumerate(update):
        for a, b in rules:
            if page != b:
                continue

            for next_page in update[i:]:
                if next_page == a:
                    return False

    return True


def get_middle_page(update: List[int]) -> int:
    middle_index = int(len(update) / 2)

    return update[middle_index]


def main():
    with Path("input.txt").open() as input_file:
        rules = []

        for line in input_file:
            if not line.strip():
                break

            a, b = [int(x) for x in line.split("|")]
            rule = (a, b)

            rules.append(rule)

        updates = []

        for line in input_file:
            update = [int(x) for x in line.split(",")]

            updates.append(update)

    valid_updates = [update for update in updates if validate(update, rules)]
    middle_pages = [get_middle_page(update) for update in valid_updates]

    count = sum(middle_pages)

    print(count)


if __name__ == '__main__':
    main()
