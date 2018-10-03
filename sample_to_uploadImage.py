import requests
from bs4 import BeautifulSoup

url = 'http://pythonscraping.com/pages/files/processing2.php'

files = {'uploadFile':open('C:/bug/static/tmp/RIMG0424.jpg','rb')}
print(files)
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryCbRNCe1YTOvGjoHS',
    'Referer':'http://pythonscraping.com/files/form2.html'
}

res_post = requests.post(url,files=files)
soup_post = BeautifulSoup(res_post.text,'html.parser')
outcome = res_post.text[8:20]
print(res_post.text[8:20])
print(res_post)
