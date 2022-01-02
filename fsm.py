from transitions import *
from transitions.extensions import *
class FSMachine(object):
    def __init__(self) -> None:
        super().__init__()
        self.states = ['Lobby','Translator','WithVoice','Chat bot','Pairing','Waiting','Paired']
        self.transitions = [
            { 'trigger': 'PressTranslatorButton', 'source': 'Lobby', 'dest': 'WithVoice','conditions':'Audio on' },
            { 'trigger': 'PressTranslatorButton', 'source': 'Lobby', 'dest': 'Translator','conditions':'Audio off' },
            { 'trigger': '!cl', 'source': 'Translator', 'dest': 'Translator' },
            { 'trigger': '!ls', 'source': 'Translator', 'dest': 'Translator' },
            { 'trigger': '!!cv 1', 'source': 'Translator', 'dest': 'WithVoice' },
            { 'trigger': '!!cv 0 ', 'source': 'WithVoice', 'dest': 'Translator' },
            { 'trigger': 'Press Chat bot Button', 'source': 'Lobby', 'dest': 'Chat bot' },
            { 'trigger': 'Press Pairing Button', 'source': 'Lobby', 'dest': 'Pairing','conditions':'haven\'t start pair' },
            { 'trigger': 'Press Pairing Button', 'source': 'Lobby', 'dest': 'Waiting','conditions':'No one else' },
            { 'trigger': 'Press Pairing Button', 'source': 'Lobby', 'dest': 'Paired','conditions':'Had Paired' },
            { 'trigger': '!find', 'source': 'Pairing', 'dest': 'Paired','conditions':'Some one else' },
            { 'trigger': '!find', 'source': 'Pairing', 'dest': 'Waiting','conditions':'No one else' },
            { 'trigger': 'λ', 'source': 'Waiting', 'dest': 'Paired','conditions':'Some one else' },
            { 'trigger': '!lobby', 'source': 'Paired', 'dest': 'Lobby' },
            { 'trigger': '!lobby', 'source': 'Waiting', 'dest': 'Lobby' },
            { 'trigger': '!lobby', 'source': 'Pairing', 'dest': 'Lobby' },
            { 'trigger': '!lobby', 'source': 'Chat bot', 'dest': 'Lobby' },
            { 'trigger': '!lobby', 'source': 'Translator', 'dest': 'Lobby' },
            { 'trigger': '!lobby', 'source': 'WithVoice', 'dest': 'Lobby' },
        ]

if __name__ == "__main__" :
    mach = FSMachine()
    machine = GraphMachine(model=mach, states=mach.states, transitions=mach.transitions,initial=mach.states[0],show_conditions=True)
    mach.get_graph().draw('img/statediagram.png', prog='dot')
    
