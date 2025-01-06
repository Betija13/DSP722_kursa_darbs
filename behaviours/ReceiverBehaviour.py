from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol, TimedBehaviour, FipaProtocol
# from sys import argv
import time

class ReceiverBehaviour(FipaRequestProtocol):
    def __init__(self, agent):
        super(ReceiverBehaviour, self).__init__(agent=agent, message=None, is_initiator=False)
        # self.agent = agent

    def handle_request(self, message):
        # print('handle_request in ReceiverBehaviour')
        display_message(self.agent.aid.localname, 'Message received: {}'.format(message.content))
        self.agent.act_upon_message(message.content)
        reply_message = self.agent.react_to_reply(message.content)
        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)

        reply.set_content(reply_message)

        if reply_message is not None:
            self.agent.send(reply)
