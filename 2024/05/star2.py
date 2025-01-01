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


def sort_by_rules(update: List[int], rules: List[Tuple[int, int]]) -> List[int]:
    sorted_update = []

    for page in update:
        last_index = len(sorted_update)

        for r1, r2 in rules:
            if r1 != page:
                continue

            if r2 not in sorted_update:
                continue

            last_index = min(last_index, sorted_update.index(r2))

        sorted_update.insert(last_index, page)

    return sorted_update


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

    invalid_updates = [update for update in updates if not validate(update, rules)]

    sorted_updates = [sort_by_rules(update, rules) for update in invalid_updates]

    middle_pages = [get_middle_page(update) for update in sorted_updates]

    count = sum(middle_pages)

    print(count)


if __name__ == '__main__':
    main()
