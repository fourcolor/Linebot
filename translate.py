import googletrans
from gtts import gTTS
class Translater:
    def __init__(self) -> None:
        self.translater = googletrans.Translator()
        self.ans = ""
        pass
    def trans(self, msg, dst):
        if(dst in googletrans.LANGCODES.values()):
            self.ans = self.translater.translate(msg, dest='zh-tw').text
        else:
            self.ans = self.translater.translate(msg, dest=dst).text
        return self.ans

    def allLanguage(self):
        return str(googletrans.LANGCODES)[1:-1].replace(',','\n').replace('\'','')

    def voice(self):
        return gTTS(self.ans)

if __name__ == "__main__":
    t = Translater()
    print(t.allLanguage())