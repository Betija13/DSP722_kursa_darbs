from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaRequestProtocol, TimedBehaviour, FipaProtocol
# from sys import argv
import time

class SenderBehaviour(FipaRequestProtocol):
    def __init__(self, agent):
        super(SenderBehaviour, self).__init__(agent=agent, message=None, is_initiator=True)

    def on_start(self):
        super(SenderBehaviour, self).on_start()

    def send_message(self, receiver_aid, message_text: str='Hello, Receiver! [first]', msg_type=ACLMessage.REQUEST):
        message = ACLMessage(msg_type)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(receiver_aid)
        message.set_content(message_text)
        self.agent.send(message)
        display_message(self.agent.aid.localname, 'Message {} sent to {}'.format(message_text, receiver_aid.name))

    def handle_inform(self, message):
        # print('handle inform in SenderBehaviour')
        display_message(self.agent.aid.localname, 'Reply received: {}'.format(message.content))
        self.agent.act_upon_message(message.content)

    def handle_failure(self, message):
        # print('handle failure in SenderBehaviour')
        display_message(self.agent.aid.localname, 'Failure received: {}'.format(message.content))
        self.agent.deal_with_failed_customer(message.content)
