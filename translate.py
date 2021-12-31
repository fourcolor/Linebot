import googletrans
from gtts import gTTS
class translater:
    def __init__(self) -> None:
        pass
    def trans(self, msg:str):
        if(msg in googletrans.LANGCODES.values()):
            return 
print(str(googletrans.LANGCODES).replace(',','\n').replace('\'',''))