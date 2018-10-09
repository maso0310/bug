import requests
from bs4 import BeautifulSoup

def post_image_to_url(path):
        url = 'http://140.113.238.34:8000/'

        proxies=[
            'http://118.178.124.33:3128',
            'http://139.129.166.68:3128',
            'http://61.143.228.162'
        ]

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Referer':'http://140.113.238.34:8000/'
        }

        res_get = requests.get(url,headers=headers,proxies={'http':random.choice(proxies)},timeout=999999999)
        soup_get = BeautifulSoup(res_get.text,'html.parser')
        csrf_value = soup_get.find('input')['value']
        print('csrftoken='+csrf_value)

        data = {'csrfmiddlewaretoken':csrf_value}
        files = {'myfile':open(path,'rb')}

        res_post = requests.post(url,files=files,headers=headers,data=data)
        soup_post = BeautifulSoup(res_post.text,'html.parser')
        outcome = soup_post.find('p')
        bug_number = outcome.text