from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests

# === LINE API 設定 ===
LINE_CHANNEL_ACCESS_TOKEN = 'eXfg4yPbTaI3pvCUcgr/bzvq6YfbUD4G1/vIvsbwuHH40GoqEquu9HyE9WHDNS/hrP9SNY4A2Fq08IojLvIHmLfOkzxYf4VyugOOGTG9VSQa8gem1KErqVcxRp/Oj6eS/LwGtX3Mf+ULe+6wwHs9ywdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'e70639183a0648790b6d35750aebaeb5'

# === Gemini 設定 ===
GEMINI_API_KEY = 'AIzaSyCrddXWVKBLg8DfqyITaXhX25ZtxJAiXMQ'
GEMINI_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'

# === Flask app ===
app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# === Webhook endpoint ===
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# === 收到文字訊息事件 ===
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text

    # 呼叫 Gemini Flash API
    gemini_response = requests.post(GEMINI_URL, json={
        "contents": [{"parts": [{"text": user_text}]}]
    })

    try:
        gemini_reply = gemini_response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        gemini_reply = "很抱歉，AI 回覆失敗了 QQ"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=gemini_reply)
    )

# === 主程式入口 ===
if __name__ == "__main__":
    app.run()