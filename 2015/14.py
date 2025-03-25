from dataclasses import dataclass

from framework.aoc import *
from utils.funcs import reverse_dict


@dataclass(frozen=True)
class Deer:
    name: str
    speed: int
    fly_time: int
    rest_time: int

    @staticmethod
    def parse(line: str) -> 'Deer':
        words = line.split()

        name = words[0]
        speed = int(words[3])
        fly_time = int(words[6])
        rest_time = int(words[13])

        return Deer(name, speed, fly_time, rest_time)

    @property
    def cycle_time(self) -> int:
        return self.fly_time + self.rest_time


deers = [Deer.parse(line) for line in INPUT.lines]

TOTAL_TIME = 2503


def __deer_distance(deer: Deer, seconds: int) -> int:
    cycle_minute = seconds % deer.cycle_time
    cycle_count = seconds // deer.cycle_time

    fly_distance = cycle_count * deer.fly_time * deer.speed

    current_cycle_distance = deer.speed * min(deer.fly_time, cycle_minute)

    current_distance = fly_distance + current_cycle_distance

    return current_distance


def star1() -> Output:
    return max(__deer_distance(deer, TOTAL_TIME) for deer in deers)


def star2() -> Output:
    points = {deer: 0 for deer in deers}

    for second in range(TOTAL_TIME):
        distances = {deer: __deer_distance(deer, second + 1) for deer in deers}

        distances = reverse_dict(distances)

        lead_deers = distances[max(distances)]

        for deer in lead_deers:
            points[deer] += 1

    return max(points.values())


if __name__ == '__main__':
    run(star1, star2)
