from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol, TimedBehaviour, FipaProtocol
# from sys import argv
import time
import re
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'
class Customer(Agent):
    def __init__(self, aid):
        super(Customer, self).__init__(aid=aid)
        self.behaviours = []
        self.behaviour_names = {}
        self.server_aid = None

    def act_upon_message(self, msg_txt: str):
        square_match = re.search(r'\[\d+\]', msg_txt)
        customer_id = square_match.group() if square_match else ''
        # print('Customer act upon msg here')
        if 'Serve food' in msg_txt:
            # print('Customer got food!')
            print(MAGENTA + f'{self.aid.name} eating' + RESET)
            time.sleep(5)
            self.behaviours[self.behaviour_names['sender']].send_message(self.server_aid, f'Meal done!! {customer_id}',
                                                                     msg_type=ACLMessage.INFORM)
        # return 'Meal done!'
        # if 'Hi' in msg_txt:
        #     print('Works!')