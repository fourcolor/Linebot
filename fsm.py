from transitions import *
from transitions.extensions import *
class FSMachine(object):
    def __init__(self) -> None:
        super().__init__()
        self.states = ['Lobby','Translator','Chat bot','Pairing','Waiting','Paired']
        self.transitions = [
            { 'trigger': 'PressTranslatorButton', 'source': 'Lobby', 'dest': 'Translator' },
            { 'trigger': '!cl [語言簡寫]->更改翻譯的語言', 'source': 'Translator', 'dest': 'Translator' },
            { 'trigger': '!ls ->顯示語言列表', 'source': 'Translator', 'dest': 'Translator' },
            { 'trigger': '!!cv 1/0 ->是否要語音', 'source': 'Translator', 'dest': 'Translator' },
            { 'trigger': 'Press Chat bot Button', 'source': 'Lobby', 'dest': 'Chat bot' },
            { 'trigger': 'Press Pairing Button', 'source': 'Lobby', 'dest': 'Pairing' },
            { 'trigger': '!find ->開始配對', 'source': 'Pairing', 'dest': 'Paired','conditions':'Some one else' },
            { 'trigger': '!find ->開始配對', 'source': 'Pairing', 'dest': 'Waiting','conditions':'No one else' },
            { 'trigger': 'λ', 'source': 'Waiting', 'dest': 'Paired','conditions':'Some one else' },
            { 'trigger': '!lobby ->回到選單', 'source': 'Paired', 'dest': 'Lobby' },
            { 'trigger': '!lobby ->回到選單', 'source': 'Waiting', 'dest': 'Lobby' },
            { 'trigger': '!lobby ->回到選單', 'source': 'Pairing', 'dest': 'Lobby' },
            { 'trigger': '!lobby ->回到選單', 'source': 'Chat bot', 'dest': 'Lobby' },
            { 'trigger': '!lobby ->回到選單', 'source': 'Translator', 'dest': 'Lobby' },
        ]

if __name__ == "__main__" :
    mach = FSMachine()
    machine = GraphMachine(model=mach, states=mach.states, transitions=mach.transitions,initial=mach.states[0])
    mach.get_graph().draw('statediagram.png', prog='dot')
    
