class Recipe:
    def __init__(self):
        self.name = ''
        self.steps = []
        self.complete = False
        self.successful = False
        self.start_time = 0
        self.end_time = 0
        self.ingredients = []
        self.customer_id = None

    def print_recipe(self):
        print('*' * 50)
        print(f'Recipe: {self.name}')
        print(f"complete: {self.complete}")
        print(f"successful: {self.successful}")
        print(f"start_time: {self.start_time}")
        print(f"end_time: {self.end_time}")
        print(f"customer_id: {self.customer_id}")
        print('*'*50)

