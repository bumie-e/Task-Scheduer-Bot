import os

from rasa_extensions.core.channels.rasa_chat import RasaChatInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

#load your trained agent
interpreter = RasaNLUInterpreter("models/nlu/default/taskbot/")
MODEL_PATH = "models/dialogue"
action_endpoint = EndpointConfig(url="https://taskbot111-actions.herokuapp.com/webhook")

agent = Agent.load(MODEL_PATH, interpreter=interpreter, action_endpoint=action_endpoint)
class MyNewInput(RasaChatInput):
    def _check_token(self, token):
        if token == 'mysecrettoken':
            return {'username': 1234}
        else:
            print("Failed to check token: {}.".format(token))
            return None

input_channel = MyNewInput(url='https://taskbot111.herokuapp.com')
# set serve_forever=False if you want to keep the server running
s = agent.handle_channels([input_channel], int(os.environ.get('PORT',5004)), serve_forever=False)