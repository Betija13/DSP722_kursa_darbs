from recepies.Recipe import Recipe
from actions.Action import Action
from actions.ActionCombination import ActionCombination
from enums.ProductStatus import ProductStatus
from enums.IngredientsName import IngredientsName
from enums.ActionNames import ActionNames

class Sushi(Recipe):
    def __init__(self):
        super().__init__()
        self.name = 'Sushi'
        self.ingredients = [
            IngredientsName.RICE.value,
            IngredientsName.SALMON.value,
            IngredientsName.SEAWEED.value,
            IngredientsName.CUCUMBER.value
        ]
        self.steps = [
            Action(
                name='BOIL rice',
                action=ActionNames.BOIL.value,
                ingredient=IngredientsName.RICE.value,
                pre_condition=ProductStatus.UNCHANGED.value
            ),
            Action(
                name='CUT fish',
                action=ActionNames.CUT.value,
                ingredient=IngredientsName.SALMON.value,
                pre_condition=ProductStatus.UNCHANGED.value
            ),
            Action(
                name='CUT cucumber',
                action=ActionNames.CUT.value,
                ingredient=IngredientsName.CUCUMBER.value,
                pre_condition=ProductStatus.UNCHANGED.value
            ),
            ActionCombination(
                name='ADD Seaweed to dish',
                action=ActionNames.ADD.value,
                ingredients=[IngredientsName.SEAWEED.value],
                pre_condition={IngredientsName.SEAWEED.value: ProductStatus.UNCHANGED.value}
            ),
            ActionCombination(
                name='PLACE rice on seaweed',
                action=ActionNames.PLACE.value,
                ingredients=[IngredientsName.RICE.value, IngredientsName.SEAWEED.value],
                pre_condition={IngredientsName.RICE.value: ProductStatus.BOILED.value, IngredientsName.SEAWEED.value: ProductStatus.PART_DISH_PROGRESS.value}
            ),
            ActionCombination(
                name='PLACE fish and cucumber on rice',
                action=ActionNames.PLACE.value,
                ingredients=[IngredientsName.SALMON.value, IngredientsName.CUCUMBER.value, IngredientsName.RICE.value],
                pre_condition={IngredientsName.SALMON.value: ProductStatus.CUT.value, IngredientsName.CUCUMBER.value: ProductStatus.CUT.value, IngredientsName.RICE.value: ProductStatus.PART_DISH_PROGRESS.value}
            ),
            ActionCombination(
                name='ROLL rice, cucumber and fish in seaweed',
                action=ActionNames.FINAL.value,
                ingredients=[IngredientsName.RICE.value, IngredientsName.SALMON.value, IngredientsName.SEAWEED.value, IngredientsName.CUCUMBER.value],
                pre_condition={IngredientsName.RICE.value: ProductStatus.PART_DISH_PROGRESS.value, IngredientsName.SALMON.value: ProductStatus.PART_DISH_PROGRESS.value, IngredientsName.SEAWEED.value: ProductStatus.PART_DISH_PROGRESS.value, IngredientsName.CUCUMBER.value: ProductStatus.PART_DISH_PROGRESS.value}
            )
        ]
