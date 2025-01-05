class Action:
    def __init__(self, name: str, action: str, ingredient: str, pre_condition: str = None):
        self.name = name
        self.action = action
        self.ingredient = ingredient
        self.pre_condition = pre_condition

