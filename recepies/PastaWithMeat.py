from recepies.Recipe import Recipe
from actions.Action import Action
from actions.ActionCombination import ActionCombination
from enums.ProductStatus import ProductStatus
from enums.IngredientsName import IngredientsName
from enums.ActionNames import ActionNames

class PastaWithMeat(Recipe):
    def __init__(self):
        super().__init__()
        self.name = 'PastaWithMeat'
        self.ingredients = [
            IngredientsName.PASTA.value,
            IngredientsName.MEAT.value
        ]
        self.steps = [
            Action(
                name='BOIL pasta',
                action=ActionNames.BOIL.value,
                ingredient=IngredientsName.PASTA.value,
                pre_condition=ProductStatus.UNCHANGED.value
            ),
            Action(
                name='CUT meat',
                action=ActionNames.CUT.value,
                ingredient=IngredientsName.MEAT.value,
                pre_condition=ProductStatus.UNCHANGED.value
            ),
            Action(
                name='COOK meat',
                action=ActionNames.COOK.value,
                ingredient=IngredientsName.MEAT.value,
                pre_condition=ProductStatus.CUT.value
            ),
            ActionCombination(
                name='COMBINE pasta and meat',
                action=ActionNames.FINAL.value,
                ingredients=[IngredientsName.PASTA.value, IngredientsName.MEAT.value],
                pre_condition={IngredientsName.PASTA.value: ProductStatus.BOILED.value, IngredientsName.MEAT.value: ProductStatus.COOKED.value}
            )
        ]
