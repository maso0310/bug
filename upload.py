import requests
import random
from bs4 import BeautifulSoup

def post_image_to_url(path):
    url = 'http://140.113.238.34:8000/'

    res_get = requests.get(url,proxies={"http":'redis://localhost:6379'})
    print(res_get)
    soup_get = BeautifulSoup(res_get.text,'html.parser')
    csrf_value = soup_get.find('input')['value']
    print('csrftoken='+csrf_value)

    data = {'csrfmiddlewaretoken':csrf_value} 
    files = {'myfile':open(path,'rb')}

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer':'http://140.113.238.34:8000/',
        'host':'ricebug.herokuapp.com',
        'Cookie':'csrftoken='+csrf_value
    }

    res_post = requests.post(url,files=files,headers=headers,data=data,proxies={"http":random.choice(proxies)},timeout=3600)
    print(res_post)
    soup_post = BeautifulSoup(res_post.text,'html.parser')
    outcome = soup_post.find_all('p')
    print(outcome)
    bug_number = outcome[1].text
    print(bug_number[9:10])
    return bug_number[9:10]