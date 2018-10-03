import apiai
import json
import requests
import random
from flask import Flask, request, abort
from imgurpython import ImgurClient
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import tempfile, os
from config import client_id, client_secret, album_id, access_token, refresh_token, line_channel_access_token, \
    line_channel_secret

app = Flask(__name__)

#各種API的認證


GOOGLE_API_KEY = os.environ.get('AIzaSyC6oj1c1hmFdluggs59FbVX5kd2t1x2MY8')
Imgur_API_SECRET = os.environ.get('1048d01dec6ca4a8b6041e609358f1c2540a144d')

ai = apiai.ApiAI('084bce6e157c47d39d5cb23715b47b69')
line_bot_api = LineBotApi('ZbWIGQOfoxOLqko0Fhh/OTjBMeeXrd+Py4xyAaNeFsa0bVP3vY05ZyOZEVj8cS9Zu+PDXGMfIUDzAGhFEjHVMN8J9ocEZsuGotbuRhzeQTML221ynVdVwXntBcIP4Ft+Sy0omAoemN84m8OxTJbFWQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('eeed6c17319b3f197e255e08bc2e98c3')

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# ================= 客製區 Start =================
def is_alphabet(uchar):
    if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a'):
        print('訊息的語言English')
        return "en"
    elif '\u4e00' <= uchar<='\u9fff':
        #print('Chinese')
        print('訊息的語言Chinese')
        return "zh-tw"
    else:
        return "en"
# ================= 客製區 End =================

@handler.add(MessageEvent, message=(TextMessage))  # default
def handle_text_message(event):                  # default
    msg = event.message.text # message from user
    uid = event.source.user_id # user id
    profile = line_bot_api.get_profile(uid)
    print(profile.display_name)
    print(profile.user_id)
    print('大頭貼網址：'+profile.picture_url)
    print(profile.status_message)

    print('使用者傳來的訊息：'+msg)
    print('使用者的ID：'+uid)

    # 1. 傳送使用者輸入到 dialogflow 上
    ai_request = ai.text_request()
    #ai_request.lang = "en"
    ai_request.lang = is_alphabet(msg)
    ai_request.session_id = uid
    ai_request.query = msg

    print('這是AI收到訊息的語言：' + ai_request.lang)
    print('這是AI收到使用者ID：' + ai_request.session_id)
    print('這是AI收到的訊息：' + ai_request.query)

    # 2. 獲得使用者的意圖
    ai_response = json.loads(ai_request.getresponse().read())
    user_intent = ai_response['result']['metadata']['intentName']
    print(ai_response),
    print('使用者意圖：' + user_intent)

    # 3. 根據使用者的意圖做相對應的回答
    if ai_request.query == "WhatToEatForLunch": # 當使用者意圖為詢問午餐時
        # 建立一個 button 的 template
        buttons_template_message = TemplateSendMessage(
            alt_text="Please tell me where you are",
            template=ButtonsTemplate(
                text="Please tell me where you are",
                actions=[
                    URITemplateAction(
                        label="Send my location",
                        uri="line://nv/location"
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            buttons_template_message)

    elif ai_request.query == "WhatToPlay": # 當使用者意圖為詢問遊戲時
        msg = "Hello, it's not ready"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))

    else: # 聽不懂時的回答
        msg = "Sorry，I don't understand"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))


@handler.add(MessageEvent, message=(ImageMessage))
def handle_message(event):
#將收到的訊息上傳至Imgur空間
    if isinstance(event.message, ImageMessage):
        print(event.message)
        ext = 'jpg'
        message_content = line_bot_api.get_message_content(event.message.id)
        uid = event.source.user_id
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
                tempfile_path = tf.name
            dist_path = tempfile_path + '.' + ext
            dist_name = os.path.basename(dist_path)
            os.rename(tempfile_path, dist_path)

        try:
            client = ImgurClient(client_id, client_secret, access_token, refresh_token)
            config = {
                'album': 'UthLp77',
                'name': 'message_content',
                'title': 'dist_name',
                'description': 'dist_path'
            }
            path = os.path.join('static', 'tmp', dist_name)
            print(path)
            client.upload_from_path(path, config=config, anon=False)

            os.remove(path)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=outcome))
        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='上傳失敗'))
            return 0

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
