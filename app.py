# 載入需要的模組
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('iYAOm73bUdqP62mH2/i+BkyAUpm4SkMnf5TlXKB7stwMnBQxvTuHPVdsrnqp+57oqtME3ElvYlSSSrlJG+YOm0fHLBEw8oiNCmNZGBXMr0K4aBArnIoenoEXlocAyQLgs0C+UOow4Q6mRAAJBpVkLAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ea97ab3bd02c52ace0e429867ef16f8f')

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
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()