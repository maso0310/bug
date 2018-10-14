#google drive api
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload


#基礎套件
import json
import time
import os

#AI自然語言分析
import apiai

#網頁爬蟲
import random
import requests
from bs4 import BeautifulSoup

from flask import Flask, request, abort

#IMGUR上傳
from imgurpython import ImgurClient

#LINEAPI
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



'''
#後台任務排程
from rq import Queue
from worker import conn
'''
app = Flask(__name__)

#各種API的認證


GOOGLE_API_KEY = os.environ.get('AIzaSyC6oj1c1hmFdluggs59FbVX5kd2t1x2MY8')
Imgur_API_SECRET = os.environ.get('1048d01dec6ca4a8b6041e609358f1c2540a144d')

ai = apiai.ApiAI('084bce6e157c47d39d5cb23715b47b69')
line_bot_api = LineBotApi('ZbWIGQOfoxOLqko0Fhh/OTjBMeeXrd+Py4xyAaNeFsa0bVP3vY05ZyOZEVj8cS9Zu+PDXGMfIUDzAGhFEjHVMN8J9ocEZsuGotbuRhzeQTML221ynVdVwXntBcIP4Ft+Sy0omAoemN84m8OxTJbFWQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('eeed6c17319b3f197e255e08bc2e98c3')

#google drive的相關文件位置
#如果要修改這些範圍，請刪除以前保存的憑據
#at~ / .credentials / drive-python-quickstart.json

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

#google drive獲得認證函數

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join('.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

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

#APP的main函數
@handler.add(MessageEvent, message=(ImageMessage))
def handle_message(event):
    #如果LINE用戶端傳送過來的是圖片
    if isinstance(event.message, ImageMessage):
    #先設定選擇的檔案附檔名
        ext = 'jpg'
        #擷取訊息內容
        message_content = line_bot_api.get_message_content(event.message.id)
        print(message_content)
        #建立臨時目錄
        with tempfile.NamedTemporaryFile(dir=static_tmp_path,'wb') as tf:
        #將臨時目錄寫入路徑tempfile_path
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name
        #臨時路徑+副檔名
        dist_path = tempfile_path + '.' + ext
        #未知
        dist_name = os.path.basename(dist_path)
        #os.rename(old,new)將舊檔名改成新檔名
        os.rename(tempfile_path, dist_path)
        path = os.path.join('static', 'tmp', dist_name)
        print("接收到的圖片路徑："+path)

        try:
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('drive', 'v3', http=http)

            results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
            else:
                print('Files:')
                for item in items:
                    print('{0} ({1})'.format(item['name'], item['id']))
            ### upload file ###
            file_metadata = {
                'name' : dist_name,
                'mimeType' : 'image/jpeg'
            }
            media = MediaFileUpload(path,mimetype='img/jpeg',resumable=True)
            file = service.files().create(body=file_metadata,media_body=media,fields='id').execute()
            print ('File ID: %s' % file.get('id'))

            os.remove(path)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='上傳成功，請等待運算結果'))
            job =  q.fetch_job(result.id)
            print(job.result)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='上傳失敗'))
        return 0




import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
