import googletrans
from gtts import gTTS
import os
class Translater:
    def __init__(self) -> None:
        self.translater = googletrans.Translator()
        self.ans = ""
        self.lan = ""
        pass
    def trans(self, msg, dst):
        if(dst in googletrans.LANGCODES.values()):
            self.lan = dst
            self.ans = self.translater.translate(msg, dest=dst).text
        else:
            self.lan = 'zh-tw'
            self.ans = self.translater.translate(msg, dest='zh-tw').text
        return self.ans

    def allLanguage(self):
        return str(googletrans.LANGCODES)[1:-1].replace(',','\n').replace('\'','')

    def voice(self):
        return gTTS(self.ans,lang = self.lan)

if __name__ == "__main__":
    t = Translater()
    print(t.trans("邂逅","en"))