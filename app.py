# 載入需要的模組
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import json
from dotenv import load_dotenv
from database import Database
from translate import translater
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
    print(event.source.user_id)
    profile = line_bot_api.get_profile(event.source.user_id)
    info = db.get(profile.user_id)
    if(info==None):
        db.insert(profile.user_id,0)
        handle_join(event)
    else:
        if(info[0] == 1):
            t = translater()
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=t.trans(event.message.text))
            )
        if (info[0] == 2):
            msg = event.message.text
            db.talk(id,msg)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text))

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
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
                        label='高雄市',
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
    

if __name__ == "__main__":
    app.run()