# 載入需要的模組
import os
from flask import Flask, request, abort
from flask.helpers import send_file, send_from_directory
from linebot import *
from linebot.exceptions import *
from linebot.models import *
import json
from dotenv import load_dotenv
from database import Database
from translate import Translater
import random as rd
import requests as rq
load_dotenv()
app = Flask(__name__)
db = Database()
# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(os.getenv('CHANNEL_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
profile = object()

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/static", methods=['GET'])
def getaudio():
    file = request.args.get('audio')
    print(file)
    try:
        return send_file(file + '.m4a')
    except:
        abort(404)

@app.route("/pairSend", methods=['POST'])
def sendMsgTo():
    id = request.values.get("id")
    msg = request.values.get("msg")
    line_bot_api.push_message(id,TextSendMessage(text=msg))

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    msg = event.message.text
    message = []
    db.talk(profile.user_id,msg)
    info = db.get(profile.user_id)
    print(info)
    if(info==None):
        db.insert(profile.user_id,0)
        handle_join(event)
    else:
        #翻譯機
        if(msg[0]=='!' or msg[0]=='！'):
            if(msg[1:6]=='lobby'):
                db.update(profile.user_id,0)
                handle_join(event)
                return
        if(info[0]==0):
            handle_join(event)
        if(info[0] == 1):
            t = Translater()
            if(msg[0]=='!' or msg[0]=='！'):
                print(msg)
                if(msg[1:5]=='help'):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                        "預設為翻成中文，可以使用下列指令執行其他功能。\n指令列\n!help       ->查詢指令\n!cl [語言簡寫]->更改翻譯的語言\n!ls         ->顯示語言列表\n!cv 1/0     ->是否要語音，1代表要，0（預設）代表不要\n!lobby      ->回到大廳\n")
                    )
                    return
                if(msg[1:3]=='cl'):
                    db.updatelanguage(profile.user_id,msg.split(' ')[1])
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                        "已將翻譯語言設定為" + msg.split(' ')[1]
                        )
                    )
                    return
                if(msg[1:3]=='ls'):
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                        t.allLanguage()
                        )
                    )
                    return
                if(msg[1:3]=='cv'):
                    enable = msg.split(' ')[1]
                    if(enable == '1'):
                        db.updateAudio(profile.user_id,True)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(
                            "語音設定為是"
                            )
                        )
                        return
                    elif(enable == '0'):
                        db.updateAudio(profile.user_id,False)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(
                            "語音設定為否"
                            )
                        )
                        return
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(
                            "必須為0或1"
                            )
                        )
                        return
            result = t.trans(event.message.text,dst=info[2])
            message.append(TextSendMessage(text=result))
            if(info[3]==True):
                t.voice().save(str(profile.user_id)+'.m4a')
                url = 'https://line-bot-fourcolor.herokuapp.com/static?audio='+str(profile.user_id)
                message.append(AudioSendMessage(url,duration=len(msg)*500))

        #聊天機器人
        if (info[0] == 2):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg)
            )
        
        if(info[0]==3):
            if(info[4]==False):
                message.append(TextSendMessage(text="請輸入!find開始配對"))
            else:
                if(msg[0]=='!' or msg[0]=='！'):
                    if(msg[1:5]=='!find'):
                        if(info[5]=='-1'):
                            cabdidates = db.getUnpaired(profile.user_id)
                            if(len(cabdidates)==0):
                                message.append(TextSendMessage(text="目前無人可配對"))
                            else:
                                selected_index = rd.randint(0,len(cabdidates)-1)
                                pairProfile = line_bot_api.get_profile(cabdidates[selected_index][0])
                                db.pair(profile.user_id,pairProfile.user_id)
                                message.append(TextSendMessage(text="配對對象： " + pairProfile.display_name))
                                data = {'id': pairProfile.user_id,'msg':"配對對象： " + profile.display_name}
                                rq.post("https://line-bot-fourcolor.herokuapp.com/pair",data=data)
                        else:
                            cabdidates = db.getUnpaired2(profile.user_id,info[5])
                            if(len(cabdidates)==0):
                                message.append(TextSendMessage(text="目前無人可配對"))
                            else:
                                selected_index = rd.randint(0,len(cabdidates)-1)
                                pairProfile = line_bot_api.get_profile(cabdidates[selected_index][0])
                                db.pair(profile.user_id,pairProfile.user_id)
                                message.append(TextSendMessage(text="配對對象： " + pairProfile.display_name))
                                data = {'id': pairProfile.user_id,'msg':"配對對象： " + profile.display_name}
                                rq.post("https://line-bot-fourcolor.herokuapp.com/pair",data=data)
                    if(msg[1:5] == 'info'):
                        if(info[5]!='-1'):
                            message.append(TextSendMessage(text="請輸入!find開始配對"))
                        else:
                            pairProfile = line_bot_api.get_profile(info[5])
                            returnMsg = "配對對象： " + pairProfile.display_name+'\n歷史對話紀錄：\n'
                            history = db.talkHistory(profile.user_id,pairProfile.user_id)
                            for i in history:
                                if(i[1]==profile.user_id):
                                    returnMsg+=(profile.display_name+':\n'+i[2]+'\n')
                                else:
                                    returnMsg+=(pairProfile.display_name+':\n'+i[2]+'\n')
                            message.append(TextSendMessage(text=returnMsg))
                else:
                    if(info[5]=='-1'):
                        message.append(TextSendMessage(text="還未配對成功"))
                    else:
                        db.talk(profile.user_id,msg,info[5])
                        line_bot_api.push_message(info[5],profile.display_name+":\n"+msg)
                        return
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

@handler.add(JoinEvent)
def handle_join(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    msg = event.message.text
    db.talk(profile.user_id,msg)
    info = db.get(profile.user_id)
    if(info==None):
        db.insert(profile.user_id,0)
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
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
    )

@handler.add(PostbackEvent)
def handle_postback(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    db.update(profile.user_id,int(event.postback.data))
    info = int(event.postback.data)
    if(info==1):
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    "預設為翻成中文，可以使用下列指令執行其他功能。\n指令列\n!help       ->查詢指令\n!cl [語言簡寫]->更改翻譯的語言\n!ls         ->顯示語言列表\n!cv 1/0     ->是否要語音，1代表要，0（預設）代表不要\n!lobby      ->回到大廳\n")
        )
    if(info==2):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                "歡迎與 Fourcolor Chatbot 聊天\n指令列\n!lobby      ->回到大廳\n")
        )
    if(info==3):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                "歡迎進入配對系統\，此系統會根據此官方帳號的進行好友配對，配對成功後便可以與對方聊天\n指令列\n!help       ->查詢指令\n!find       ->開始配對（或是重新配對）\n!info       ->查看配對資訊及歷史對話紀錄\n!lobby      ->回到大廳\n")
        )

if __name__ == "__main__":
    app.run()