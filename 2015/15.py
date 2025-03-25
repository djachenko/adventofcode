from collections import defaultdict
from functools import cache
from typing import Dict, Iterable

from frozendict import frozendict

from framework.aoc import *
from utils.funcs import mul

Ingredient = Dict[str, int]


def __parse_ingredients() -> Iterable[Ingredient]:
    for line in INPUT.lines:
        name, properties = line.split(": ")

        properties = properties.split(", ")
        properties = [p.split() for p in properties]

        properties = {n: int(a) for n, a in properties}

        yield frozendict(properties)


ingredients = list(__parse_ingredients())

TEASPOONS_COUNT = 100

Seq = frozendict


def __score_of_combination(combination: Seq[Ingredient, int]) -> int:
    amounts = defaultdict(lambda: 0)

    for ingredient, count in combination.items():
        for prop, amount in ingredient.items():
            amounts[prop] += amount * count

    del amounts["calories"]

    for key in amounts:
        amounts[key] = max(amounts[key], 0)

    result = mul(amounts.values())

    return result


@cache
def __combine_ingredients(combination: Seq[Ingredient, int]) -> int:
    if sum(combination.values()) == TEASPOONS_COUNT:
        return __score_of_combination(combination)

    max_score = 0

    for ingredient in ingredients:
        new_combination = combination.set(ingredient, combination[ingredient] + 1)

        max_score = max(max_score, __combine_ingredients(new_combination))

    return max_score


@cache
def combine_ingredients_with_calories(combination: Seq[Ingredient, int]) -> int:
    if sum(combination.values()) == TEASPOONS_COUNT:
        if sum(ingredient["calories"] * count for ingredient, count in combination.items()) == 500:
            return __score_of_combination(combination)
        else:
            return 0

    max_score = 0

    for ingredient in ingredients:
        new_combination = combination.set(ingredient, combination[ingredient] + 1)

        max_score = max(max_score, combine_ingredients_with_calories(new_combination))

    return max_score


def star1() -> Output:
    return __combine_ingredients(frozendict({ingredient: 0 for ingredient in ingredients}))


def star2() -> Output:
    return combine_ingredients_with_calories(frozendict({ingredient: 0 for ingredient in ingredients}))


if __name__ == '__main__':
    run(star1, star2)
