from recepies.Recipe import Recipe
from actions.Action import Action
from actions.ActionCombination import ActionCombination
from enums.ProductStatus import ProductStatus
from enums.IngredientsName import IngredientsName


class Salad(Recipe):
    def __init__(self):
        super().__init__()
        self.name = 'Salad'
        self.ingredients = [
            IngredientsName.LETTUCE.value,
            IngredientsName.TOMATO.value,
            IngredientsName.CUCUMBER.value
        ]
        self.steps = [
            Action(
                name='CUT lettuce',
                action='CUT',
                ingredient=IngredientsName.LETTUCE.value,
                pre_condition=ProductStatus.UNCHANGED.value
            ),
            Action(
                name='CUT tomato',
                action='CUT',
                ingredient=IngredientsName.TOMATO.value,
                pre_condition=ProductStatus.UNCHANGED.value
            ),
            Action(
                name='CUT cucumber',
                action='CUT',
                ingredient=IngredientsName.CUCUMBER.value,
                pre_condition=ProductStatus.UNCHANGED.value
            ),
            ActionCombination(
                name='MIX all ingredients',
                action='FINAL',
                ingredients=[IngredientsName.LETTUCE.value, IngredientsName.TOMATO.value, IngredientsName.CUCUMBER.value],
                pre_condition={IngredientsName.LETTUCE.value: ProductStatus.CUT.value, IngredientsName.TOMATO.value: ProductStatus.CUT.value, IngredientsName.CUCUMBER.value: ProductStatus.CUT.value}
            )
        ]