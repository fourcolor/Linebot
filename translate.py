import googletrans
from gtts import gTTS
import os
class Translater:
    def __init__(self) -> None:
        self.translater = googletrans.Translator()
        self.ans = ""
        pass
    def trans(self, msg, dst):
        if(dst in googletrans.LANGCODES.values()):
            self.ans = self.translater.translate(msg, dest=dst).text
        else:
            self.ans = self.translater.translate(msg, dest='zh-tw').text
        return self.ans

    def allLanguage(self):
        return str(googletrans.LANGCODES)[1:-1].replace(',','\n').replace('\'','')

    def voice(self):
        return gTTS(self.ans)

if __name__ == "__main__":
    t = Translater()
    print(t.trans("你好",""))
    t.voice().save('static/'+'aslkdjlsakdjasij'+'.m4a')