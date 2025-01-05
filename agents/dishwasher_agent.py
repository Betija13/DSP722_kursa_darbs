from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol, TimedBehaviour, FipaProtocol
# from sys import argv
import time
import re
from enums.MessageTexts import MessageTexts

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'

class DishwasherAgent(Agent):
    def __init__(self, aid):
        super(DishwasherAgent, self).__init__(aid=aid)
        # self.receiver_aid = receiver_aid
        # self.other_cook_aid = None
        # self.server_aid = None
        # self.dishwasher_aid = None
        self.behaviours = []
        self.behaviour_names = {}
        # self.behaviours.append(SenderBehaviour(self))
        # self.msg_count = 0
        # self.inventory = None
        self.work_area = None

    def react_to_reply(self, msg_txt: str):
        # print('Dishwasher react_to_reply here: ', msg_txt)
        square_match = re.search(r'\[\d+\]', msg_txt)
        customer_id = square_match.group() if square_match else ''
        if MessageTexts.NEED_CLEAN_DISHES.value in msg_txt:
            self.wash_dishes()
            return f'{MessageTexts.DISHES_DONE.value} {customer_id}'
        print('aaaaaa----: ',msg_txt)
        if 'Helaaaalo' in msg_txt:
            return 'Hi, Cook!'
        elif 'Hi' in msg_txt:
            return 'Works!'

    def act_upon_message(self, msg_txt: str):
        pass
        # print('Dishwasher act upon msg here: ', msg_txt)
        # square_match = re.search(r'\[\d+\]', msg_txt)
        # customer_id = square_match.group() if square_match else ''
        # if MessageTexts.NEED_CLEAN_DISHES.value in msg_txt:
        #     time.sleep(3)
        #     return f'Done! :) {customer_id}'

    def wash_dishes(self):
        print(MAGENTA + f'{self.aid.name} washing dishes' + RESET)
        # self.work_area.print_work_area()
        if self.work_area.dirty_dishes > 0:
            self.work_area.dirty_dishes -= 1
            time.sleep(2)
            self.work_area.clean_dishes += 1
        else:
            print('No dirty dishes to wash!')

    # def move_dishes_to_inventory(self):
    #     pass