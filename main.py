from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol, TimedBehaviour, FipaProtocol
# from sys import argv
import time
from agents.cook_agent import CookAgent
from agents.server_agent import ServerAgent
from agents.dishwasher_agent import DishwasherAgent
from agents.customer import Customer
from behaviours.SenderBehaviour import SenderBehaviour
from behaviours.ReceiverBehaviour import ReceiverBehaviour
from behaviours.ClientBehaviour import ClientBehaviour
from restaurant.Inventory import Inventory
from restaurant.WorkArea import WorkArea

if __name__ == '__main__':
    restaurant_inventory = Inventory()
    restaurant_work_area = WorkArea()

    cook_1_aid = AID(name='cook_1@localhost:20000')
    cook_1_agent = CookAgent(cook_1_aid)
    cook_1_agent.inventory = restaurant_inventory
    cook_1_agent.work_area = restaurant_work_area

    server_aid = AID(name='server@localhost:20100')
    server_agent = ServerAgent(server_aid)

    customer = Customer(AID(name='customer@localhost:20200'))

    server_agent.behaviours.append(ReceiverBehaviour(server_agent))
    server_agent.behaviour_names['receiver'] = len(server_agent.behaviours) - 1
    server_agent.behaviours.append(SenderBehaviour(server_agent))
    server_agent.behaviour_names['sender'] = len(server_agent.behaviours) - 1
    server_agent.cook_1_aid = cook_1_aid
    # server_agent.behaviours.append(SenderBehaviour(server_agent, server_aid))
    # server_agent.behaviours.append(ClientBehaviour(server_agent, receiver_aid=server_aid))
    customer.behaviours.append(ClientBehaviour(customer, receiver_aid=server_aid))
    customer.behaviour_names['client'] = len(customer.behaviours) - 1
    customer.behaviours.append(SenderBehaviour(customer))
    customer.behaviour_names['sender'] = len(customer.behaviours) - 1
    customer.server_aid = server_aid

    cook_1_agent.behaviours.append(SenderBehaviour(cook_1_agent))
    cook_1_agent.behaviour_names['sender'] = len(cook_1_agent.behaviours) - 1
    cook_1_agent.behaviours.append(ReceiverBehaviour(cook_1_agent))
    cook_1_agent.behaviour_names['receiver'] = len(cook_1_agent.behaviours) - 1

    cook_2_aid = AID(name='cook_2@localhost:20300')
    cook_2_agent = CookAgent(cook_2_aid)
    cook_2_agent.inventory = restaurant_inventory
    cook_2_agent.work_area = restaurant_work_area

    cook_1_agent.other_cook_aid = cook_2_aid
    cook_2_agent.other_cook_aid = cook_1_aid
    cook_1_agent.server_aid = server_aid
    cook_2_agent.server_aid = server_aid
    server_agent.customer_aid = customer.aid

    cook_2_agent.behaviours.append(ReceiverBehaviour(cook_2_agent))
    cook_2_agent.behaviour_names['receiver'] = len(cook_2_agent.behaviours) - 1

    cook_2_agent.behaviours.append(SenderBehaviour(cook_2_agent))
    cook_2_agent.behaviour_names['sender'] = len(cook_2_agent.behaviours) - 1

    dishwasher_aid = AID(name='dishwasher@localhost:20400')
    dishwasher_agent = DishwasherAgent(dishwasher_aid)
    dishwasher_agent.behaviours.append(ReceiverBehaviour(dishwasher_agent))
    dishwasher_agent.behaviour_names['receiver'] = len(dishwasher_agent.behaviours) - 1
    server_agent.dishwasher_aid = dishwasher_aid
    dishwasher_agent.inventory = restaurant_inventory
    dishwasher_agent.work_area = restaurant_work_area
    server_agent.work_area = restaurant_work_area

    start_loop([cook_1_agent, server_agent, customer, cook_2_agent, dishwasher_agent])
