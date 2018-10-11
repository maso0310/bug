import requests
import random
from bs4 import BeautifulSoup  
  
url = 'http://pythonscraping.com/files/form2.html/'


res_get = requests.get(url,proxies={"https":'https://203.104.146.152'})
print(res_get)
soup_get = BeautifulSoup(res_get.text,'html.parser')
csrf_value = soup_get.find('input')['value']
print('csrftoken='+csrf_value)

data = {'csrfmiddlewaretoken':csrf_value}
files = {'myfile':open("397892.jpg",'rb')}

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer':'http://140.113.238.34:8000/',
    'Cookie':'csrftoken='+csrf_value
}

res_post = requests.post(url,files=files,headers=headers,data=data,proxies={"https":'https://203.104.146.152'})
print(res_post)
soup_post = BeautifulSoup(res_post.text,'html.parser')
outcome = soup_post.find_all('p')
print(outcome)
bug_number = outcome[1].text
print(bug_number[9:10])