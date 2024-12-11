from pathlib import Path


def main():
    with Path("input.txt").open() as input_file:
        string = input_file.read()

    stones = [int(c) for c in string.split()]

    blink_count = 25

    for blink in range(blink_count):
        new_stones = []

        for stone in stones:
            str_stone = str(stone)
            str_stone_length = len(str_stone)

            if stone == 0:
                new_stones.append(1)
            elif str_stone_length % 2 == 0:
                new_stones += [
                    int(str_stone[:int(str_stone_length / 2)]),
                    int(str_stone[int(str_stone_length / 2):])
                ]
            else:
                new_stones.append(stone * 2024)

        stones = new_stones

        print(f"{blink}: {len(stones)}")

    print(len(stones))


if __name__ == '__main__':
    main()
