import random
from typing import Final


def is_contained_in(value, list):
    for item in list:
        if value in list:
            return True
    return False


def calculate_macro_calories(protiens, fats, carbs):
    protiens_cals: Final = 4
    carbs_cals: Final = 4
    fats_cals: Final = 9

    return protiens * protiens_cals + carbs * carbs_cals + fats * fats_cals


def choose_random_number_in_range(min, max):
    return random.randint(min, max)
