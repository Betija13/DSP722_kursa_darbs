from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol, TimedBehaviour, FipaProtocol
# from sys import argv
import time
import re
from recepies.Sushi import Sushi
from recepies.PastaWithMeat import PastaWithMeat
from recepies.Salad import Salad
from enums.ProductStatus import ProductStatus
from actions.Action import Action
from actions.ActionCombination import ActionCombination
from enums.IngredientsName import IngredientsName
from enums.MessageTexts import MessageTexts
from enums.ActionNames import ActionNames

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'


class CookAgent(Agent):
    def __init__(self, aid):
        super(CookAgent, self).__init__(aid=aid)
        # self.receiver_aid = receiver_aid
        self.other_cook_aid = None
        self.server_aid = None
        # self.dishwasher_aid = None
        self.behaviours = []
        self.behaviour_names = {}
        self.inventory = None
        self.work_area = None
        self.cooks_inventory = []
        self.customers_recipes = {}

    def act_upon_message(self, msg_txt: str):
        square_match = re.search(r'\[\d+\]', msg_txt)
        customer_id = square_match.group() if square_match else ''
        brackets_match = re.search(r'\(([^)]+)\)', msg_txt)
        start_time = brackets_match.group(1) if brackets_match else ''
        # print(f'Cook act upon msg here: {msg_txt}')
        if MessageTexts.FOOD_WANTED.value in msg_txt:
            # print(f'start_time: {start_time}')
            self.customers_recipes[customer_id] = 'in_progress'
            order = msg_txt.split(':')[-1].strip()
            # print(f'received food wanted : {order}!')
            recipe = self.get_recipe_of_food(order, start_time)
            if recipe:
                recipe.customer_id = customer_id
                self.work_area.recipes.append(recipe)

                # The main cook divides steps and sends to other cook what he has to do
                my_steps, other_steps = self.decide_upon_steps(recipe)
                message_text = f'{customer_id}R: {recipe.name};S: {", ".join([step.name for step in other_steps])}'
                self.behaviours[self.behaviour_names['sender']].send_message(self.other_cook_aid, message_text, msg_type=ACLMessage.REQUEST)
                my_steps_simple_actions = [step for step in my_steps if isinstance(step, Action)]
                # print(f'{self.aid.name} My steps: {len(my_steps_simple_actions)}')
                steps_done = self.make_food(my_steps_simple_actions)
                # print(f'{self.aid.name} Steps done: {steps_done}')
                self.customers_recipes[customer_id] = 'done'
                # print(f'{self.aid.name} customers recipes: {self.customers_recipes}')
                if steps_done is None:
                    print(RED + f'{customer_id} FAILED' + RESET)
                    self.behaviours[self.behaviour_names['sender']].send_message(self.server_aid,
                                                                                 f'{MessageTexts.FAILED_FOOD.value} {customer_id}',
                                                                                 msg_type=ACLMessage.FAILURE)

            else:
                self.customers_recipes[customer_id] = 'done'
                self.behaviours[self.behaviour_names['sender']].send_message(self.server_aid,
                                                                             f'{MessageTexts.FAILED_FOOD.value} {customer_id}',
                                                                             msg_type=ACLMessage.FAILURE)

        elif MessageTexts.STEPS_DONE.value in msg_txt:
            # TODO improve
            square_match = re.search(r'\[\d+\]', msg_txt)
            customer_id = square_match.group().strip() if square_match else ''
            recipe_name = msg_txt.split()[2].strip()
            # print(f'{self.aid.name} Cook received  customer_id: {customer_id} recipe_name: {recipe_name}')
            recipe = self.get_recipe_of_food(recipe_name)
            if recipe:
                cooks_status = self.customers_recipes[customer_id]
                # print(f'{self.aid.name} Cooks status: {cooks_status}')
                retries = 0
                while cooks_status != 'done' and retries < 3:
                    # print(f'{self.aid.name} Cooks status: {cooks_status}')
                    # print(f'{self.aid.name} customers recipes: {self.customers_recipes}')
                    print(YELLOW + f'{customer_id} Main cook not done yet, waiting for 4' + RESET)
                    print('waiting for 4')
                    time.sleep(4)
                    retries += 1
                    cooks_status = self.customers_recipes[customer_id]
                    # print(f'{self.aid.name} Cooks status: {cooks_status}')
                    # print(f'{self.aid.name} customers recipes: {self.customers_recipes}')
                if cooks_status == 'done':
                    customers_recipe = None
                    customers_recipes = [rec for rec in self.work_area.recipes if rec.customer_id == customer_id]
                    if len(customers_recipes) > 0:
                        customers_recipe = customers_recipes[0]
                    if customers_recipe:
                        self.work_area.recipes.remove(customers_recipe)
                        customers_recipe.complete = True
                        self.work_area.recipes.append(customers_recipe)
                    my_steps, other_steps = self.decide_upon_steps(recipe)
                    steps_combinations = [step for step in my_steps if isinstance(step, ActionCombination)]
                    food_served_complete = self.serve_food(steps_combinations)
                    if food_served_complete:
                        customers_recipe = None
                        customers_recipes = [rec for rec in self.work_area.recipes if rec.customer_id == customer_id]
                        if len(customers_recipes) > 0:
                            customers_recipe = customers_recipes[0]
                        if customers_recipe:
                            self.work_area.recipes.remove(customers_recipe)
                            valid_dish_products = [
                                self.get_product_from_work_area(name, ProductStatus.DISH_READY.value) for name in
                                customers_recipe.ingredients]
                            if None not in valid_dish_products:
                                customers_recipe.successful = True
                            self.work_area.recipes.append(customers_recipe)
                        self.behaviours[self.behaviour_names['sender']].send_message(self.server_aid,
                                                                                     f'{MessageTexts.FOOD_DONE.value} {recipe.name} {customer_id}',
                                                                                     msg_type=ACLMessage.INFORM)
                    else:
                        print(RED + f'{customer_id} FAILED food_served_complete' + RESET)
                        self.behaviours[self.behaviour_names['sender']].send_message(self.server_aid,
                                                                                     f'Failed dish! {recipe.name} {customer_id}',
                                                                                     msg_type=ACLMessage.FAILURE)
                else:
                    print(RED + f'{customer_id} FAILED cooks_status' + RESET)
                    self.behaviours[self.behaviour_names['sender']].send_message(self.server_aid,
                                                                                 f'Failed dish! {recipe_name} {customer_id}',
                                                                                 msg_type=ACLMessage.FAILURE)
            else:
                print(RED + f'{self.aid.name} No recipe found' + RESET)
                self.behaviours[self.behaviour_names['sender']].send_message(self.server_aid,
                                                                             f'Failed dish! {recipe_name} {customer_id}',
                                                                             msg_type=ACLMessage.FAILURE)
            # self.behaviours[self.behaviour_names['sender']].send_message(self.server_aid, f'Food done! {customer_id}',
            #                                                              msg_type=ACLMessage.INFORM)
        elif MessageTexts.FAILED_FOOD.value in msg_txt.lower():
            self.behaviours[self.behaviour_names['sender']].send_message(self.server_aid,
                                                                         f'{MessageTexts.FAILED_FOOD.value} {customer_id}',
                                                                         msg_type=ACLMessage.FAILURE)

        elif 'Hi' in msg_txt:
            print('Works!')

    def react_to_reply(self, msg_txt: str):
        if 'R:' in msg_txt and 'S:' in msg_txt:
            recipie_name, step_names = msg_txt.split(';')
            customer_id = re.search(r'\[\d+\]', recipie_name).group()
            recipie_name = recipie_name.replace(customer_id, '').strip()
            recipie_name = recipie_name.split(':')[-1].strip()
            recipe = self.get_recipe_of_food(name=recipie_name)
            my_steps = []
            if recipe:
                steps = step_names.split(':')[-1].strip().split(',')
                for step in steps:
                    for recipe_step in recipe.steps:
                        if step.strip() in recipe_step.name:
                            my_steps.append(recipe_step)
                steps_done = self.make_food(my_steps)
                if steps_done is None:
                    print(RED + f'{customer_id} FAILED react_to_reply steps_done' + RESET)
                    return f'{MessageTexts.FAILED_FOOD.value} {customer_id}'
                else:
                    return_str = f'{customer_id} {MessageTexts.STEPS_DONE.value} {recipe.name} {len(my_steps)} steps.'
                    return return_str
            else:
                return f'{MessageTexts.FAILED_FOOD.value} {customer_id}'

    def get_recipe_of_food(self, name: str, start_time: str = None):
        pasta_with_meat = PastaWithMeat()
        sushi = Sushi()
        salad = Salad()
        if name == pasta_with_meat.name:
            recipe = pasta_with_meat
        elif name == sushi.name:
            recipe = sushi
        elif name == salad.name:
            recipe = salad
        else:
            print(RED + f'{self.aid.name}No recipe found for {name}' + RESET)
            return None
        if start_time:
            recipe.start_time = start_time
        return recipe

    def decide_upon_steps(self, recipe):
        my_steps = []
        other_steps = []
        pasta_with_meat = PastaWithMeat()
        sushi = Sushi()
        salad = Salad()
        # TODO make more flexible
        my_steps_idx = []
        if recipe.name == pasta_with_meat.name:
            my_steps_idx = [0, 3]
        elif recipe.name == sushi.name:
            my_steps_idx = [0, 3, 4, 5, 6]
        elif recipe.name == salad.name:
            my_steps_idx = [2, 3]

        for idx, step in enumerate(recipe.steps):
            if idx in my_steps_idx:
                my_steps.append(step)
            else:
                other_steps.append(step)
        return my_steps, other_steps

    def make_food(self, steps):
        # print(f'{self.aid.name} Making food! Gping through {len(steps)} steps')
        made_food = []

        for action_step in steps:
            action = action_step.action
            ingredient = action_step.ingredient
            pre_condition = action_step.pre_condition
            # print(f'{self.aid.name} action: {action} ingredient: {ingredient} pre_condition: {pre_condition}')
            if pre_condition == ProductStatus.UNCHANGED.value:
                self.get_product_ingredients(ingredient)
            # Check if product already in inventory
            valid_products = [item for item in self.cooks_inventory if item.name == ingredient and item.status == pre_condition]
            if len(valid_products) == 0:
                self.get_product_ingredients(ingredient)
            valid_products = [item for item in self.cooks_inventory if
                              item.name == ingredient and item.status == pre_condition]
            current_product = valid_products[0] if valid_products else None
            if current_product in made_food:
                made_food.remove(current_product)
            if current_product is None:
                print(RED + f'{self.aid.name} current_product is None. action: {action} ingredient: {ingredient} pre_condition: {pre_condition}' + RESET)
                return None
            else:
                self.cooks_inventory.remove(current_product)
                if action == ActionNames.CUT.value:
                    current_product = self.cut_product(current_product)
                    if current_product.status != ProductStatus.CUT.value:
                        print(RED + f'{self.aid.name} unsuccessful cut' + RESET)
                        return None
                elif action == ActionNames.COOK.value:
                    current_product = self.cook_product(current_product)
                    if current_product.status != ProductStatus.COOKED.value:
                        print(RED + f'{self.aid.name} unsuccessful cook' + RESET)
                        return None
                elif action == ActionNames.BOIL.value:
                    current_product = self.boil_product(current_product)
                    if current_product.status != ProductStatus.BOILED.value:
                        print(RED + f'{self.aid.name} unsuccessful boil' + RESET)
                        return None
                self.cooks_inventory.append(current_product)

                made_food.append(current_product)
        for food_item in made_food:
            self.add_product_to_work_area(food_item)
        return made_food

    def add_product_to_work_area(self, product):
        if product.name == IngredientsName.LETTUCE.value:
            self.work_area.lettuce.append(product)
        elif product.name == IngredientsName.TOMATO.value:
            self.work_area.tomato.append(product)
        elif product.name == IngredientsName.CUCUMBER.value:
            self.work_area.cucumber.append(product)
        elif product.name == IngredientsName.RICE.value:
            self.work_area.rice.append(product)
        elif product.name == IngredientsName.SEAWEED.value:
            self.work_area.seaweed.append(product)
        elif product.name == IngredientsName.SALMON.value:
            self.work_area.salmon.append(product)
        elif product.name == IngredientsName.MEAT.value:
            self.work_area.meat.append(product)
        elif product.name == IngredientsName.PASTA.value:
            self.work_area.pasta.append(product)
        else:
            print(RED + f"WEIRD PRODUCT {product.name}!" + RESET)

    def get_product_ingredients(self, product):
        if product == IngredientsName.LETTUCE.value:
            if len(self.inventory.lettuce) > 0:
                self.cooks_inventory.append(self.inventory.lettuce.pop())
        elif product == IngredientsName.TOMATO.value:
            if len(self.inventory.tomato) > 0:
                self.cooks_inventory.append(self.inventory.tomato.pop())
        elif product == IngredientsName.CUCUMBER.value:
            if len(self.inventory.cucumber) > 0:
                self.cooks_inventory.append(self.inventory.cucumber.pop())
        elif product == IngredientsName.RICE.value:
            if len(self.inventory.rice) > 0:
                self.cooks_inventory.append(self.inventory.rice.pop())
        elif product == IngredientsName.SEAWEED.value:
            if len(self.inventory.seaweed) > 0:
                self.cooks_inventory.append(self.inventory.seaweed.pop())
        elif product == IngredientsName.SALMON.value:
            if len(self.inventory.salmon) > 0:
                self.cooks_inventory.append(self.inventory.salmon.pop())
        elif product == IngredientsName.MEAT.value:
            if len(self.inventory.meat) > 0:
                self.cooks_inventory.append(self.inventory.meat.pop())
        elif product == IngredientsName.PASTA.value:
            if len(self.inventory.pasta) > 0:
                self.cooks_inventory.append(self.inventory.pasta.pop())
        else:
            print(RED + f"WEIRD PRODUCT {product}!" + RESET)

    def cut_product(self, product):
        product_cut = False
        tries = 0
        while not product_cut and tries < 3:
            if self.work_area.available_cutting_board > 0:
                self.work_area.available_cutting_board -= 1
                print(MAGENTA + f'{self.aid.name} cutting {product.name}' + RESET)
                time.sleep(2)
                product_cut = True
                self.work_area.available_cutting_board += 1
            else:
                tries += 1
                print(YELLOW + f'{self.aid.name} waiting for cutting board' + RESET)
                time.sleep(4)

        if product_cut:
            product.status = ProductStatus.CUT.value
        else:
            print(RED + f'{self.aid.name} product not cut' + RESET)
        return product

    def cook_product(self, product):
        product_cooked = False
        tries = 0
        while not product_cooked and tries < 3:
            if self.work_area.available_pans > 0:
                self.work_area.available_pans -= 1
                print(MAGENTA + f'{self.aid.name} cooking {product.name}' + RESET)
                time.sleep(3)
                product_cooked = True
                self.work_area.available_pans += 1
            else:
                tries += 1
                print(YELLOW + f'{self.aid.name} waiting for available pan' + RESET)
                time.sleep(4)
        if product_cooked:
            product.status = ProductStatus.COOKED.value
        else:
            print(RED + f'{self.aid.name} product not cooked' + RESET)
        return product

    def serve_food(self, steps_combinations):
        everything_successful = True
        clean_dish = self.get_clean_dish()
        if not clean_dish:
            everything_successful = False
        else:
            for step in steps_combinations:
                ingredients = step.ingredients
                pre_conditions = step.pre_conditions

                if ProductStatus.UNCHANGED.value in pre_conditions.values():
                    unchanged_ingredients = [key for key, value in pre_conditions.items() if value == ProductStatus.UNCHANGED.value]
                    for ingredient in unchanged_ingredients:
                        self.get_product_ingredients(ingredient)
                        valid_products = [item for item in self.cooks_inventory if
                                          item.name == ingredient and item.status == ProductStatus.UNCHANGED.value]
                        current_product = valid_products[0] if valid_products else None
                        if current_product is not None:
                            self.cooks_inventory.remove(current_product)
                            self.add_product_to_work_area(current_product)
                valid_products = [self.get_product_from_work_area(name, status) for name, status in pre_conditions.items()]
                if len(valid_products) != len(ingredients) or None in valid_products:
                    print(RED + f'{self.aid.name} Everything was not successful!' + RESET)
                    everything_successful = False
                    # self.work_area.print_work_area()
                    for v_product in valid_products:
                        if v_product is not None:
                            self.add_product_to_work_area(v_product)

                else:
                    for product in valid_products:
                        if step.action == ActionNames.FINAL.value:
                            product.status = ProductStatus.DISH_READY.value
                            self.add_product_to_work_area(product)
                        else:
                            product.status = ProductStatus.PART_DISH_PROGRESS.value
                            self.add_product_to_work_area(product)
        return everything_successful

    def get_product_from_work_area(self, product_name, product_status):
        returned_product = None
        if product_name == IngredientsName.LETTUCE.value:
            valid_products = [item for item in self.work_area.lettuce if item.status == product_status]
            if len(valid_products) > 0:
                returned_product = valid_products[0]
                self.work_area.lettuce.remove(returned_product)
        elif product_name == IngredientsName.TOMATO.value:
            valid_products = [item for item in self.work_area.tomato if item.status == product_status]
            if len(valid_products) > 0:
                returned_product = valid_products[0]
                self.work_area.tomato.remove(returned_product)
        elif product_name == IngredientsName.CUCUMBER.value:
            valid_products = [item for item in self.work_area.cucumber if item.status == product_status]
            if len(valid_products) > 0:
                returned_product = valid_products[0]
                self.work_area.cucumber.remove(returned_product)
        elif product_name == IngredientsName.RICE.value:
            valid_products = [item for item in self.work_area.rice if item.status == product_status]
            if len(valid_products) > 0:
                returned_product = valid_products[0]
                self.work_area.rice.remove(returned_product)
        elif product_name == IngredientsName.SEAWEED.value:
            valid_products = [item for item in self.work_area.seaweed if item.status == product_status]
            if len(valid_products) > 0:
                returned_product = valid_products[0]
                self.work_area.seaweed.remove(returned_product)
        elif product_name == IngredientsName.SALMON.value:
            valid_products = [item for item in self.work_area.salmon if item.status == product_status]
            if len(valid_products) > 0:
                returned_product = valid_products[0]
                self.work_area.salmon.remove(returned_product)
        elif product_name == IngredientsName.MEAT.value:
            valid_products = [item for item in self.work_area.meat if item.status == product_status]
            if len(valid_products) > 0:
                returned_product = valid_products[0]
                self.work_area.meat.remove(returned_product)
        elif product_name == IngredientsName.PASTA.value:
            valid_products = [item for item in self.work_area.pasta if item.status == product_status]
            if len(valid_products) > 0:
                returned_product = valid_products[0]
                self.work_area.pasta.remove(returned_product)
        else:
            print(RED + f"WEIRD PRODUCT {product_name}!" + RESET)
        return returned_product

    def boil_product(self, product):
        product_boiled = False
        tries = 0
        while not product_boiled and tries < 3:
            if self.work_area.available_boiler > 0:
                self.work_area.available_boiler -= 1
                print(MAGENTA + f'{self.aid.name} boiling {product.name}' + RESET)
                time.sleep(3)
                product_boiled = True
                self.work_area.available_boiler += 1
            else:
                print(YELLOW + f'{self.aid.name} waiting for available boiler' + RESET)
                tries += 1
                time.sleep(4)
        if product_boiled:
            product.status = ProductStatus.BOILED.value
        else:
            print(RED + f'{self.aid.name} product not boiled' + RESET)
        return product

    def get_clean_dish(self):
        print(MAGENTA + f'{self.aid.name} getting clean dish' + RESET)
        dish = False
        tries = 0
        while not dish and tries < 3:
            if self.work_area.clean_dishes > 0:
                self.work_area.clean_dishes -= 1
                dish = True
            else:
                print(YELLOW + f'{self.aid.name} waiting for clean dish' + RESET)
                tries += 1
                time.sleep(3)
        if not dish:
            print(RED + f'{self.aid.name} no clean dish' + RESET)
        return dish


