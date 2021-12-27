# 載入需要的模組
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('iYAOm73bUdqP62mH2/i+BkyAUpm4SkMnf5TlXKB7stwMnBQxvTuHPVdsrnqp+57oqtME3ElvYlSSSrlJG+YOm0fHLBEw8oiNCmNZGBXMr0K4aBArnIoenoEXlocAyQLgs0C+UOow4Q6mRAAJBpVkLAdB04t89/1O/w1cDnyilFU=')
handler = WebhookParser('ea97ab3bd02c52ace0e429867ef16f8f')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run()