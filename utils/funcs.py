from math import log10
from typing import Iterable, List, TypeVar, Callable, Dict


def split_int(a: int) -> (int, int):
    length = digits_in_int(a)

    splitter = pow(10, length / 2)

    return int(a / splitter), int(a % splitter)


def digits_in_int(a: int) -> int:
    if a == 0:
        return 1

    return int(log10(a)) + 1


T = TypeVar("T")
V = TypeVar("V")


def first(seq: Iterable[T], predicate: Callable[[T], bool] = lambda: True) -> T | None:
    for i in seq:
        if predicate(i):
            return i

    return None


def chunks(seq: List[T], n: int) -> Iterable[List[T]]:
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def reverse_dict(d: Dict[T, V]) -> Dict[V, List[T]]:
    result = {}

    for key, value in d.items():
        if value not in result:
            result[value] = []

        result[value].append(key)

    return result


def reverse_dict_single(d: Dict[T, V]) -> Dict[V, T]:
    assert is_unique(d.values())

    return {value: key for key, value in d.items()}


def is_unique(s: Iterable[T]) -> bool:
    cache = set()

    for e in s:
        if e in cache:
            return False

        cache.add(e)

    return True


def unique(s: Iterable[T]) -> List[T]:
    cache = set()
    unique_s = []

    for e in s:
        if e in cache:
            continue

        cache.add(e)
        unique_s.append(e)

    return unique_s
