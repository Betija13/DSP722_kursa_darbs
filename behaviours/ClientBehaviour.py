import random
import time

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol
from pade.behaviours.protocols import TimedBehaviour
from recepies.Sushi import Sushi
from recepies.PastaWithMeat import PastaWithMeat
from recepies.Salad import Salad

from datetime import datetime
from sys import argv

class ClientBehaviour(TimedBehaviour):

    def __init__(self, agent, receiver_aid, time_s: float = 10.0):
        super(ClientBehaviour, self).__init__(agent, time_s)
        self.customer_count = 0
        self.order_choices = [PastaWithMeat().name, Sushi().name, Salad().name, PastaWithMeat().name, Sushi().name, Salad().name]

        self.client_entered_message = ACLMessage(ACLMessage.INFORM)
        self.client_entered_message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        self.client_entered_message.add_receiver(receiver_aid)
        self.client_entered_message.set_content('customer_entered')

        self.client_order_message = ACLMessage(ACLMessage.REQUEST)
        self.client_order_message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        self.client_order_message.add_receiver(receiver_aid)
        self.client_order_message.set_content(f'customer_order: {self.order_choices[0]}')

        # self.closing_msg = ACLMessage(ACLMessage.INFORM)
        # self.closing_msg.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        # self.closing_msg.add_receiver(receiver_aid)
        # self.closing_msg.set_content('customers_done')


    def on_time(self):
        super(ClientBehaviour, self).on_time()
        # print(f"From client behaviour instance tables: {self.agent.agentInstance.table}")
        self.customer_count += 1
        if len(self.order_choices) > 0:
        #     self.order_choices = ['pasta with meat', 'sushi', 'salad']
        # if self.customer_count - 1 >= self.max_customers:
        #     if self.customer_count - 1 == self.max_customers:
        #         self.agent.send(self.closing_msg)
        # else:
            self.client_entered_message.set_content(f'customer_entered [{self.customer_count}]')
            self.agent.send(self.client_entered_message)
            # print(f'\n\n-------------------\nsending entered {self.client_entered_message}\n\n-------------------')
            # print(f'sending order {self.order}')
            time.sleep(3.0)
            order = self.order_choices.pop()
            order_time = datetime.now().strftime('%H:%M:%S')
            self.client_order_message.set_content(f'customer_order [{self.customer_count}] ({order_time}): {order}')
            self.agent.send(self.client_order_message)
            # self.agent.call_later(3.0, lambda: self.agent.send(self.client_order_message))
            # print(f'\n\n-------------------\nclient_order_message {self.client_order_message}\n\n-------------------')


