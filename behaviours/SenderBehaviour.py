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
        # self.first_receiver = first_receiver

        # self.agent = agent

    def on_start(self):
        super(SenderBehaviour, self).on_start()
        # print(f'SenderBehaviour started {self.agent.aid.name}')
        # time.sleep(3)
        # for i in range(10):
        #     time.sleep(5)
        #     print(f'waiting 5 {i} ')
        # self.agent.agentInstance.register_agent(self.agent)
        # print(self.agent.agentInstance.table)
        # self.agent.call_later(5.0, lambda: self.send_message(self.first_receiver, 'Hello!'))
        # self.send_message(message_text='First? message!')

    def send_message(self, receiver_aid, message_text: str='Hello, Receiver! [first]', msg_type=ACLMessage.REQUEST):
        message = ACLMessage(msg_type)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(receiver_aid)
        message.set_content(message_text)
        self.agent.send(message)
        # self.agent.msg_count += 1
        # print(self.agent.agentInstance.table)
        display_message(self.agent.aid.localname, 'Message {} sent to {}'.format(message_text, receiver_aid.name))


    def handle_inform(self, message):
        # print('handle inform in SenderBehaviour')
        display_message(self.agent.aid.localname, 'Reply received: {}'.format(message.content))
        self.agent.act_upon_message(message.content)
        # if message.content == 'Hello, Sender!':
        #     self.send_message('Hello again, Receiver  =)!')
        # Message received

    def handle_failure(self, message):
        # print('handle failure in SenderBehaviour')
        display_message(self.agent.aid.localname, 'Failure received: {}'.format(message.content))
        self.agent.deal_with_failed_customer(message.content)
        # self.agent.act_upon_message(message.content)