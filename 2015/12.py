import json

from framework.aoc import *

JSON_INPUT = json.loads(INPUT.line)


def __sum_visit(json_object) -> int:
    if isinstance(json_object, int):
        return json_object
    elif isinstance(json_object, str):
        return 0
    elif isinstance(json_object, list):
        return sum(__sum_visit(i) for i in json_object)
    elif isinstance(json_object, dict):
        return sum(__sum_visit(i) for i in json_object.values())
    else:
        assert False


def __sum_visit_without_red(json_object) -> int:
    if isinstance(json_object, int):
        return json_object
    elif isinstance(json_object, str):
        return 0
    elif isinstance(json_object, list):
        return sum(__sum_visit_without_red(i) for i in json_object)
    elif isinstance(json_object, dict):
        values = json_object.values()

        if "red" in values:
            return 0
        else:
            return sum(__sum_visit_without_red(i) for i in values)
    else:
        assert False


def star1() -> Output:
    return __sum_visit(JSON_INPUT)


def star2() -> Output:
    return __sum_visit_without_red(JSON_INPUT)


if __name__ == '__main__':
    run(star1, star2)
