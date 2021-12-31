# 載入需要的模組
import os
from flask import Flask, request, abort
from linebot import *
from linebot.exceptions import *
from linebot.models import *
import json
from dotenv import load_dotenv
from database import Database
from translate import Translater
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
        if(info[0] == 1):
            t = Translater()
            message.append(TextSendMessage(text=t.trans(event.message.text,dst=info[2])))
            if(info[3]==True):
                t.voice().save('static/'+str(profile.user_id)+'m4a')
                url = 'https://line-bot-fourcolor.herokuapp.com/static/'+str(profile.user_id)+'m4a'
                message.append(AudioSendMessage('static/'+str(profile.user_id)+'m4a',duration=len(msg)*500))
        if (info[0] == 2):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )
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
                "歡迎與 Fourcolor Chatbot 聊天\n\
                指令列\
                !lobby      ->回到大廳\n")
        )
    if(info==3):
        pass

if __name__ == "__main__":
    app.run()