from mimetypes import init
from google.protobuf import message
from transitions import *
from transitions.extensions import *
from linebot.models import *
from database import Database
from translate import Translater
from Chatbot import *
import random as rd
import requests as rq
class FSMachine(object):
    def __init__(self,profile,info,line_bot_api) -> None:
        super().__init__()
        self.states = ['Lobby','Translator','Chat bot','Pairing','Waiting','Paired']
        self.db = Database()
        self.profile = profile
        self.line_bot_api = line_bot_api
        if(info==None):
            self.db.insert(profile.user_id,0)
            self.state = self.states[info[0]]
        else:
            self.state = self.states[info[0]]
            if(info[0]==3 and info[4]!=False):
                if(info[5]!='-1'):
                    self.state = self.states[5]
                else:
                    self.state = self.states[4]
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
        self.machine = GraphMachine(model=self, states=self.states, transitions=self.transitions,initial=self.states)

    def chooseMainState(self,state):
        state = int(state)
        self.db.update(self.profile.user_id,state)
        message = []
        if(state==0):
            self.PressTranslatorButton(self)
        if(state==1):
            message.append(self.PressTranslatorButton(self))
        if(state==2):
            message.append(self.PressChatbotButton(self))
        if(state==3):
            message.append(self.PressPairingButton(self))
        return message

    def golobby(self):
        self.state = self.states[0]
        return TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://scontent.ftpe7-4.fna.fbcdn.net/v/t1.18169-9/10408779_612698742164619_7012016086151051936_n.jpg?_nc_cat=103&ccb=1-5&_nc_sid=174925&_nc_ohc=_Z77ruHvqE8AX-kqAZl&_nc_ht=scontent.ftpe7-4.fna&oh=00_AT_FoEzERCaSrdnQTjRiV-FXOMMiDo0xwlzxNN3qvbUrbg&oe=61F6A36C',
                    title='Menu',
                    text='功能選單',
                    actions=[
                        PostbackTemplateAction(
                            label = '翻譯-Translate',
                            data = '1'
                        ),
                        PostbackTemplateAction(
                            label='聊天機器人-Chatbot',
                            data = '2'
                        ),
                        PostbackTemplateAction(
                            label='配對系統-Pairing',
                            data = '3'
                        )
                    ]
                )
            )


    def PressTranslatorButton(self):
        self.state = self.states[1]
        return TextSendMessage(
            "預設為翻成中文，可以使用下列指令執行其他功能。\n指令列\n!help       ->查詢指令\n!cl [語言簡寫]->更改翻譯的語言\n!ls         ->顯示語言列表\n!cv 1/0     ->是否要語音，1代表要，0（預設）代表不要\n!lobby      ->回到大廳\n")

    def PressChatbotButton(self):
        self.state = self.states[2]
        return TextSendMessage(
            "歡迎與 Fourcolor Chatbot 聊天\n指令列\n!lobby      ->回到大廳\n")        

    def PressPairingButton(self):
        self.state = self.states[3]
        return TextSendMessage(
            "歡迎進入配對系統\，此系統會根據此官方帳號的進行好友配對，配對成功後便可以與對方聊天\n指令列\n!help       ->查詢指令\n!find       ->開始配對（或是重新配對）\n!info       ->查看配對資訊及歷史對話紀錄\n!lobby      ->回到大廳\n")
    def MessageIn(self,msg):
        message = []
        if(self.info==None):
            self.db.insert(self.profile.user_id,0)
            message.append(self.golobby())
        else:
            #翻譯機
            if(self.state == 1):
                message.append(self.TranslaterState(msg))
            #聊天機器人
            if (self.state == 2):
                 message.append(self.ChatBotSate(msg))
            #配對系統
            if(self.state == 3):
                message.append(self.PairingState)
               
        return message

    def TranslaterState(self,msg):
        message = []
        if(msg[0]=='!' or msg[0]=='！'):
            if(msg[1:6]=='lobby'):
                self.db.update(self.profile.user_id,0)
                message.append(self.golobby())
                return
        if(self.info[0]==0):
            message.append(self.golobby())
        if(self.info[0] == 1):
            t = Translater()
            if(msg[0]=='!' or msg[0]=='！'):
                print(msg)
                if(msg[1:5]=='help'):
                    message.append( 
                        TextSendMessage(
                        "預設為翻成中文，可以使用下列指令執行其他功能。\n指令列\n!help       ->查詢指令\n!cl [語言簡寫]->更改翻譯的語言\n!ls         ->顯示語言列表\n!cv 1/0     ->是否要語音，1代表要，0（預設）代表不要\n!lobby      ->回到大廳\n")
                    )
                if(msg[1:3]=='cl'):
                    self.db.updatelanguage(self.profile.user_id,msg.split(' ')[1])
                    message.append(
                        TextSendMessage(
                        "已將翻譯語言設定為" + msg.split(' ')[1]
                        )
                    )
                if(msg[1:3]=='ls'):
                    message.append(
                        TextSendMessage(
                        t.allLanguage()
                        )
                    )
                if(msg[1:3]=='cv'):
                    enable = msg.split(' ')[1]
                    if(enable == '1'):
                        self.db.updateAudio(self.profile.user_id,True)
                        message.append(
                            TextSendMessage(
                            "語音設定為開啟"
                            )
                        )
                    elif(enable == '0'):
                        self.db.updateAudio(self.profile.user_id,False)
                        self.db.updateAudio(self.profile.user_id,True)
                        message.append(
                            TextSendMessage(
                            "語音設定為關閉"
                            )
                        )
                    else:
                        message.append(
                            TextSendMessage(
                            "必須為0或1"
                            )
                        )
            result = t.trans(msg,dst=self.info[2])
            message.append(TextSendMessage(text=result))
            if(self.info[3]==True):
                t.voice().save(str(self.profile.user_id)+'.m4a')
                url = 'https://line-bot-fourcolor.herokuapp.com/static?audio='+str(self.profile.user_id)
                message.append(AudioSendMessage(url,duration=len(msg)*500))
        return message

    def ChatBotSate(self,msg):
        message = []
        t = chatModel()
        message.append(TextSendMessage(t.talk(msg)))
        return message
    
    def PairingState(self,msg):
        message = []
        if(msg[0]=='!' or msg[0]=='！'):
            if(msg[1:5]=='find'):
                self.db.enablePairing(self.profile.user_id)
                if(self.info[5]=='-1'):
                    cabdidates = self.db.getUnpaired(self.profile.user_id)
                    if(len(cabdidates)==0):
                        message.append(TextSendMessage(text="目前無人可配對"))
                    else:
                        selected_index = rd.randint(0,len(cabdidates)-1)
                        pairProfile = self.line_bot_api.get_profile(cabdidates[selected_index][0])
                        self.db.pair(self.profile.user_id,pairProfile.user_id)
                        message.append(TextSendMessage(text="配對對象： " + pairProfile.display_name))
                        data = {'id': pairProfile.user_id,'msg':"配對對象： " + self.profile.display_name}
                        rq.post("https://line-bot-fourcolor.herokuapp.com/pairSend",data=data)
                else:
                    cabdidates = self.db.getUnpaired2(self.profile.user_id,self.info[5])
                    if(len(cabdidates)==0):
                        message.append(TextSendMessage(text="目前無人可配對"))
                    else:
                        self.db.rmPairing(self.info[5])
                        data = {'id': self.info[5],'msg':self.profile.display_name+" 取消了配對"}
                        rq.post("https://line-bot-fourcolor.herokuapp.com/pairSend",data=data)
                        selected_index = rd.randint(0,len(cabdidates)-1)
                        pairProfile = self.ine_bot_api.get_profile(cabdidates[selected_index][0])
                        self.db.pair(self.profile.user_id,pairProfile.user_id)
                        message.append(TextSendMessage(text="配對對象： " + pairProfile.display_name))
                        data = {'id': pairProfile.user_id,'msg':"配對對象： " + self.profile.display_name}
                        rq.post("https://line-bot-fourcolor.herokuapp.com/pairSend",data=data)
            if(msg[1:5] == 'info'):
                if(self.info[5]=='-1'):
                    message.append(TextSendMessage(text="請輸入!find開始配對"))
                else:
                    pairProfile = self.line_bot_api.get_profile(self.info[5])
                    returnMsg = "配對對象： " + pairProfile.display_name+'\n歷史對話紀錄：\n'
                    history = self.db.talkHistory(self.profile.user_id,pairProfile.user_id)
                    for i in history:
                        if(i[1]==self.profile.user_id):
                            returnMsg+=(self.profile.display_name+':\n'+i[2]+'\n')
                        else:
                            returnMsg+=(pairProfile.display_name+':\n'+i[2]+'\n')
                    message.append(TextSendMessage(text=returnMsg))
        else:
            if(self.info[4]==False):
                message.append(TextSendMessage(text="請輸入!find開始配對"))
            else:
                if(self.info[5]=='-1'):
                    message.append(TextSendMessage(text="還未配對成功"))
                else:
                    self.db.talk(self.profile.user_id,msg,self.info[5])
                    self.line_bot_api.push_message(self.info[5],TextSendMessage(self.profile.display_name+":\n"+msg))
        return message
