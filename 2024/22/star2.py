from collections import defaultdict

from utils import read_by_line


def mix(value: int, secret_number: int) -> int:
    return secret_number ^ value


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def main():
    start_numbers = []

    for line in read_by_line():
        start_numbers.append(int(line))

    sum_caches = defaultdict(lambda: 0)

    for number in start_numbers:
        seq = tuple(None for _ in range(4))

        seller_caches = {}

        for i in range(2000):
            saved_number = number

            number = prune(mix(number * 64, number))
            number = prune(mix(number // 32, number))
            number = prune(mix(number * 2048, number))

            saved_digit = saved_number % 10
            new_digit = number % 10

            diff = new_digit - saved_digit

            seq = *seq[1:], diff

            if i >= 3 and seq not in seller_caches:
                seller_caches[seq] = new_digit

        for seq, price in seller_caches.items():
            sum_caches[seq] += price

    print(max(sum_caches.values()))


if __name__ == '__main__':
    main()
