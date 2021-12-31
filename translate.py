import googletrans
from gtts import gTTS
class Translater:
    def __init__(self) -> None:
        self.translater = googletrans.Translator()
        self.ans = ""
        pass
    def trans(self, msg, dst):
        if(dst in googletrans.LANGCODES.values()):
            ans = self.translater.translate(msg, dest='zh-tw').text
            return ans
        else:
            return self.translater.translate(msg, dest=dst).text

    def allLanguage(self):
        return str(googletrans.LANGCODES).replace(',','\n').replace('\'','')

    def voice(self):
        return gTTS(self.ans)