import inspect
import time
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path

from utils.funcs import first
from utils.inputs import Input, WebInput

Output = str | int | None
Task = Callable[[], Output]


@lru_cache()
def __determine_day_and_year() -> (int, int):
    stack = inspect.stack()
    filenames = [s.filename for s in stack]

    caller_file = first(filenames, lambda n: not (n.startswith("<") or n == __file__))
    caller_path = Path(caller_file)

    file_name = caller_path.stem
    parent_name = caller_path.parent.name

    day = int(file_name)
    year = int(parent_name)

    return day, year


def __build_input() -> Input:
    day, year = __determine_day_and_year()

    return WebInput(year, day)


INPUT = __build_input()


def __run_and_measure(task: Task, title: str) -> None:
    start_time = time.time()

    result = task()

    end_time = time.time()

    total_time = end_time - start_time
    total_time = round(total_time, 5)

    if result:
        print(f"{title}: {result} in {total_time} s.")
    else:
        print(f"{title} not solved.")


def run(star1: Task, star2: Task) -> None:
    day, year = __determine_day_and_year()

    print(f"{year}, day {day}:")

    __run_and_measure(star1, "First")
    __run_and_measure(star2, "Second")
