from Ingredients.Product import Product
from enums.IngredientsName import IngredientsName


class Meat(Product):
    def __init__(self):
        super().__init__()
        self.name = IngredientsName.MEAT.value
