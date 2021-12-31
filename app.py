# 載入需要的模組
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import json
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

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
    print(body)
    id = json.loads(body)["events"][0]["source"]["userId"]
    print(id)

    # handle webhook body
    try:
        profile = line_bot_api.get_profile(id)
        print(profile)
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
'''
@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "謝謝邀請我這個機器來至此群組！！我會盡力為大家服務的～"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )

if __name__ == "__main__":
    app.run()