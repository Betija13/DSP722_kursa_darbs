from enum import Enum


class ProductStatus(Enum):
    UNCHANGED = 'unchanged'
    CUT = 'cut'
    COOKED = 'cooked'
    BOILED = 'boiled'
    PART_DISH_PROGRESS = 'part_dish_progress'
    DISH_READY = 'dish_ready'