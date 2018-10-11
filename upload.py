import requests
import random
from bs4 import BeautifulSoup

def post_image_to_url(path):
    url = 'http://140.113.238.34:8000/'

    res_get = requests.get(url)
    soup_get = BeautifulSoup(res_get.text,'html.parser')
    csrf_value = soup_get.find('input')['value']
    print('csrftoken='+csrf_value)
    print(res_get)

    data = {'csrfmiddlewaretoken':csrf_value}
    files = {'myfile':open("397892.jpg",'rb')}

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer':'http://140.113.238.34:8000/',
        'Cookie':'csrftoken='+csrf_value,
        "Connection": "keep-alive"
    }

    proxies=[
        'http://112.25.41.136:80',
        'http://61.143.228.162',
        'http://127.0.0.1:9743'
    ]
    time.sleep(1)
    res_post = requests.post(url,files=files,proxies=random.choice(proxies),headers=headers,data=data)
    print(res_post)
    soup_post = BeautifulSoup(res_post.text,'html.parser')
    outcome = soup_post.find_all('p')
    print(outcome)
    bug_number = outcome[1].text
    print(bug_number)
    return bug_number[9:10]