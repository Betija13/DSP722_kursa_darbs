
class WorkArea:
    def __init__(self):
        self.clean_dishes = 5
        self.dirty_dishes = 0
        self.available_pans = 2
        self.available_boiler = 2
        self.available_cutting_board = 2
        self.meat = []
        self.pasta = []
        self.cucumber = []
        self.rice = []
        self.seaweed = []
        self.salmon = []
        self.lettuce = []
        self.tomato = []
        self.meals = []
        self.recipes = []
        self.score = 0
        self.total_possible_score = 0
        self.time_for_dish = 60
        self.total_score_food = 2
        self.total_score_time = 1

    def print_work_area(self):
        print('-' * 100)
        print(f'Clean dishes: {self.clean_dishes}')
        print(f'Dirty dishes: {self.dirty_dishes}')
        print(f'Available pans: {self.available_pans}')
        print(f'Available boiler: {self.available_boiler}')
        print(f'Available cutting board: {self.available_cutting_board}')
        print(f'Meat: {[(obj.name, obj.status) for obj in self.meat]}')
        print(f'Pasta: {[(obj.name, obj.status) for obj in self.pasta]}')
        print(f'Cucumber: {[(obj.name, obj.status) for obj in self.cucumber]}')
        print(f'Rice: {[(obj.name, obj.status) for obj in self.rice]}')
        print(f'Seaweed: {[(obj.name, obj.status) for obj in self.seaweed]}')
        print(f'Salmon: {[(obj.name, obj.status) for obj in self.salmon]}')
        print(f'Lettuce: {[(obj.name, obj.status) for obj in self.lettuce]}')
        print(f'Tomato: {[(obj.name, obj.status) for obj in self.tomato]}')
        print(f'Meals: {[(obj.name, obj.status) for obj in self.meals]}')
        print(f'Recipes: {len(self.recipes)}')
        for recipie_obj in self.recipes:
            recipie_obj.print_recipe()
        print('-' * 100)

