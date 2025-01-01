from utils import read_by_line


def mix(value: int, secret_number: int) -> int:
    return secret_number ^ value


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def main():
    start_numbers = []

    for line in read_by_line():
        start_numbers.append(int(line))

    total_sum = 0

    for number in start_numbers:
        for i in range(2000):
            number = prune(mix(number * 64, number))
            number = prune(mix(number // 32, number))
            number = prune(mix(number * 2048, number))

        total_sum += number

    print(total_sum)


if __name__ == '__main__':
    main()
