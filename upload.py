import requests
import random
from bs4 import BeautifulSoup

def post_image_to_url(path):
    url = 'http://140.113.238.34:8000/'

    proxies=[
        'http://97.90.251.228:8080',
        'http://104.248.208.209:8080',
        'http://142.93.77.16:8080',
        'http://68.183.26.106:8080',
        'http://159.203.58.149:8080',
        'http://216.167.165.77:8080',
        'http://209.234.102.87:8080'
    ]


    res_get = requests.get(url)
    print(res_get)
    soup_get = BeautifulSoup(res_get.text,'html.parser')
    csrf_value = soup_get.find('input')['value']
    print('csrftoken='+csrf_value)


    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer':'http://140.113.238.34:8000/',
        'Cookie':'csrftoken='+csrf_value,
        "Connection": "close"
    }

    data = {'csrfmiddlewaretoken':csrf_value}
    files = {'myfile':open(path,'rb')}

    res_post = requests.post(url,files=files,proxies={'http':random.choice(proxies)},headers=headers,data=data,timeout=1200)
    print(res_post)
    soup_post = BeautifulSoup(res_post.text,'html.parser')
    outcome = soup_post.find_all('p')
    print(outcome)
    bug_number = outcome[1].text
    print(bug_number)
    return bug_number[9:10]