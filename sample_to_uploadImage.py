import requests
from bs4 import BeautifulSoup

url = 'http://pythonscraping.com/pages/files/processing2.php'

files = {'uploadFile':open('C:/bug/static/tmp/RIMG0424.jpg','rb')}

print(files)

res_post = requests.post(url,files=files)
soup_post = BeautifulSoup(res_post.text,'html.parser')
outcome = res_post.text[8:20]
print(res_post.text[8:20])
print(res_post)
