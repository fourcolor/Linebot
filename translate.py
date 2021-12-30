import googletrans
from gtts import gTTS
class translater:
    def __init__(self) -> None:
        pass
    def trans(self, msg:str):
        msg[:2].lower()
        if(msg in googletrans.LANGCODES.values()):
            return 
tts = gTTS('の')
tts.save('hello.mp3')