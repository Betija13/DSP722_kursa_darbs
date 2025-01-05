from Ingredients.Meat import Meat
from Ingredients.Pasta import Pasta
from Ingredients.Cucumber import Cucumber
from Ingredients.Rice import Rice
from Ingredients.Seaweed import Seaweed
from Ingredients.Salmon import Salmon
from Ingredients.Lettuce import Lettuce
from Ingredients.Tomato import Tomato


class Inventory:
    def __init__(
            self,
            count_meat: int = 5,
            count_pasta: int = 5,
            count_cucumber: int = 2,
            count_rice: int = 5,
            count_seaweed: int = 5,
            count_salmon: int = 5,
            count_lettuce: int = 5,
            count_tomato: int = 5
    ):
        self.meat = [Meat() for i in range(count_meat)]
        self.pasta = [Pasta() for i in range(count_pasta)]
        self.cucumber = [Cucumber() for i in range(count_cucumber)]
        self.rice = [Rice() for i in range(count_rice)]
        self.seaweed = [Seaweed() for i in range(count_seaweed)]
        self.salmon = [Salmon() for i in range(count_salmon)]
        self.lettuce = [Lettuce() for i in range(count_lettuce)]
        self.tomato = [Tomato() for i in range(count_tomato)]
