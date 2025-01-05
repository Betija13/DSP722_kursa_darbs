from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol, TimedBehaviour, FipaProtocol
from enums.MessageTexts import MessageTexts
# from sys import argv
import time
import re
from datetime import datetime

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'

class ServerAgent(Agent):
    def __init__(self, aid):
        super(ServerAgent, self).__init__(aid=aid)
        # self.receiver_aid = receiver_aid
        self.cook_1_aid = None
        # self.server_aid = None
        self.dishwasher_aid = None
        self.customer_aid = None
        self.behaviours = []
        self.behaviour_names = {}
        # self.behaviours.append(SenderBehaviour(self))
        # self.msg_count = 0
        self.customers = 0
        # self.served_customers = []
        self.work_area = None


    def act_upon_message(self, msg_txt: str):
        square_match = re.search(r'\[\d+\]', msg_txt)
        customer_id = square_match.group() if square_match else ''
        brackets_match = re.search(r'\(([^)]+)\)', msg_txt)
        start_time = brackets_match.group() if brackets_match else ''
        # print(f'Server act upon msg here: {msg_txt}')
        if MessageTexts.CUSTOMER_ENTERED.value in msg_txt:
            self.customers += 1
            # print(f'From ServerAgent, got customer_entered, customers: {self.customers}')
        elif MessageTexts.CUSTOMER_ORDER.value in msg_txt:
            order = msg_txt.split(':')[-1].strip()
            print(MAGENTA + f'{self.aid.name} informing cook of customers desire {order}' + RESET)
            self.behaviours[self.behaviour_names['sender']].send_message(self.cook_1_aid, f'{MessageTexts.FOOD_WANTED.value} {customer_id} {start_time}: {order}')
            # print(f'sent to cook food wanted: {order}!')
        elif MessageTexts.FOOD_DONE.value in msg_txt:
            # print(f'From ServerAgent, got Food done!, customers: {self.customers}')
            # if customer_id not in self.served_customers:
            #     self.served_customers.append(customer_id)
            print(MAGENTA + f'{self.aid.name} serving food {customer_id}' + RESET)
            time.sleep(1.5)
            customers_recipe = None
            customers_recipes = [rec for rec in self.work_area.recipes if rec.customer_id == customer_id]
            if len(customers_recipes) > 0:
                customers_recipe = customers_recipes[0]
                if customers_recipe:
                    order_time = datetime.now().strftime('%H:%M:%S')
                    customers_recipe.end_time = order_time
                    successful = self.calculate_results(customers_recipe)
                    if successful:
                        self.behaviours[self.behaviour_names['sender']].send_message(self.customer_aid, f'{MessageTexts.SERVE_FOOD.value} {customer_id}',
                                                                                     msg_type=ACLMessage.INFORM)
                    else:
                        # customers_recipe.print_recipe()
                        # self.work_area.print_work_area()
                        self.get_dishes()
                        self.behaviours[self.behaviour_names['sender']].send_message(self.dishwasher_aid,
                                                                                     f'{MessageTexts.NEED_CLEAN_DISHES.value} {customer_id}')
                        self.customers -= 1
                        self.output_score_info()


                    # TODO else: still need to collect dishes
            # else:
            #     print(f"CUSTOMER {customer_id} ALREADY SERVED!")
        elif MessageTexts.MEAL_DONE.value in msg_txt:
            # if customer_id not in self.cleaned_dishes:
            #     self.cleaned_dishes.append(customer_id)
            self.get_dishes()
            self.behaviours[self.behaviour_names['sender']].send_message(self.dishwasher_aid, f'{MessageTexts.NEED_CLEAN_DISHES.value} {customer_id}')
            self.customers -= 1
            # else:
            #     print(f"CUSTOMER {customer_id} ALREADY CLEANED DISHES!")
        elif MessageTexts.DISHES_DONE.value in msg_txt:
            # self.work_area.print_work_area()
            self.output_score_info()

    def output_score_info(self):
        total_score = self.work_area.score / self.work_area.total_possible_score
        stars = 0
        if total_score > 0.5:
            stars += 1
        if total_score > 0.75:
            stars += 1
        if total_score > 0.9:
            stars += 1
        print_text = f'score: {self.work_area.score} ' \
                     f'\t total_possible_score: {self.work_area.total_possible_score} ' \
                     f'\t Total score {total_score}\t Rating: {stars} stars'
        if stars == 0:
            print(RED + print_text + RESET)
        elif stars == 1:
            print(YELLOW + print_text + RESET)
        elif stars == 2:
            print(GREEN + print_text + RESET)
        elif stars == 3:
            print(BLUE + print_text + RESET)
        else:
            print(MAGENTA + print_text + RESET)

    def react_to_reply(self, msg_txt: str):
        print(f'Server react_to_reply here: {msg_txt}')
        if 'Hello' in msg_txt:
            return 'Hi, Cook!'
        elif 'Hi' in msg_txt:
            return 'Works!'

    def calculate_results(self, recipe):
        try:

            self.work_area.recipes.remove(recipe)
            recipe_successful = recipe.successful
            if recipe_successful:

                end_time = datetime.strptime(recipe.end_time, '%H:%M:%S')
                start_time = datetime.strptime(recipe.start_time, '%H:%M:%S')
                time_difference = end_time - start_time
                time_difference_in_seconds = time_difference.total_seconds()
                if time_difference_in_seconds < self.work_area.time_for_dish:
                    recipe_successful = True
                    score = self.work_area.total_score_food + self.work_area.total_score_time * ((self.work_area.time_for_dish - time_difference_in_seconds)/ self.work_area.time_for_dish)
                    self.work_area.score += score
                    self.work_area.total_possible_score += self.work_area.total_score_food + self.work_area.total_score_time
                    print(CYAN + f'{recipe.customer_id} This recipes score: {score}\t Total score: {self.work_area.score}\t time_difference_in_seconds: {time_difference_in_seconds}' + RESET)
                else:
                    print(RED + f'{recipe.customer_id} This recipes score: 0\tTotal score: {self.work_area.score}\ttime_difference_in_seconds: {time_difference_in_seconds}' + RESET)
                    self.work_area.total_possible_score += self.work_area.total_score_food + self.work_area.total_score_time
                    recipe_successful = False
            else:
                print(
                    RED + f'{recipe.customer_id} This recipes score: 0\tTotal score: {self.work_area.score}\t recepie unsuccssesful' + RESET)
                self.work_area.total_possible_score += self.work_area.total_score_food + self.work_area.total_score_time
                recipe_successful = False
        except Exception as e:
            print(RED + f'Error in calculate_results: {e}' + RESET)
            recipe_successful = False
        return recipe_successful


    def get_dishes(self):
        time.sleep(1)
        self.work_area.dirty_dishes += 1

    def deal_with_failed_customer(self, msg_text):
        # print(MAGENTA + f'Failed customer: {msg_text}' + RESET)
        # self.work_area.print_work_area()

        square_match = re.search(r'\[\d+\]', msg_text)
        customer_id = square_match.group() if square_match else ''
        customers_recipe = None
        customers_recipes = [rec for rec in self.work_area.recipes if rec.customer_id == customer_id]
        if len(customers_recipes) > 0:
            customers_recipe = customers_recipes[0]
        if customers_recipe:
            # customers_recipe.print_recipe()
            customers_recipe.successful = False
            # self.work_area.recipes.remove(customers_recipe)
            # customers_recipe.complete = True
            # self.work_area.recipes.append(customers_recipe)
            self.calculate_results(customers_recipe)
            # self.get_dishes()
            # self.behaviours[self.behaviour_names['sender']].send_message(self.dishwasher_aid,
            #                                                              f'need_clean_dishes {customer_id}')
            # self.work_area.recipes.remove(customers_recipe)
            self.customers -= 1

