import requests
import random
from bs4 import BeautifulSoup  


#目標URL
url = 'http://140.113.238.34:8000/'
#獲取目標URL的CSRFVALUE
res_get = requests.get(url)
print(res_get)
soup_get = BeautifulSoup(res_get.text,'html.parser')
csrf_value = soup_get.find('input')['value']
print('csrftoken='+csrf_value)

#透過GOOGLE硬碟將檔案下載至本地
from __future__ import print_function
import httplib2
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_img(credentials,file_id):

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    #下載檔案至根目錄
    #file_id = '1ltXFMCEpGwgMyevrepGTch95VH9Wx1if'
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_id+'.jpg','wb')
    downloader = MediaIoBaseDownload(fh, request)
    print(downloader)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))

    #設置要POST的訊息
    data = {'csrfmiddlewaretoken':csrf_value}
    files = {'uploadFile':open(file_id+'.jpg','rb')}
    print(files)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer':'http://140.113.238.34:8000/',
        'Cookie':'csrftoken='+csrf_value
    }
    res_post = requests.post(url,data=data,headers=headers,files=files)
    print(res_post)
    soup_post = BeautifulSoup(res_post.text,'html.parser')
    outcome = soup_post.text
    #print(outcome)
    #bug_number = outcome
    #print(bug_number)