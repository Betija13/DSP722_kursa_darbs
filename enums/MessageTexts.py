from enum import Enum


class MessageTexts(Enum):
    CUSTOMER_ENTERED = 'customer_entered'
    CUSTOMER_ORDER = 'customer_order'
    FOOD_WANTED = 'food_wanted'
    SERVE_FOOD = 'serve_food'
    NEED_CLEAN_DISHES = 'need_clean_dishes'
    DISHES_DONE = 'dishes_done'
    MEAL_DONE = 'meal_done'
    FOOD_DONE = 'food_done'
    STEPS_DONE = 'steps_done'
    FAILED_FOOD = 'failed_food'
