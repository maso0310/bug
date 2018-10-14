import requests
import random
from bs4 import BeautifulSoup  
  
url = 'http://140.113.238.34:8000/'

res_get = requests.get(url)
print(res_get)
soup_get = BeautifulSoup(res_get.text,'html.parser')
csrf_value = soup_get.find('input')['value']
print('csrftoken='+csrf_value)

data = {'csrfmiddlewaretoken':csrf_value}
files = {'uploadFile':open("RIMG0424.JPG",'rb')}
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