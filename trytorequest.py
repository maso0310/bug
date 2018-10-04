import requests
from bs4 import BeautifulSoup

url = 'https://tw.shop.com/maso0310'

headers = {
    'Connection ':'keep-alive',
    'Content-Encoding':'gzip',
    'Content-Language':'zh-TW',
    'Content-Length':'46471',
    'Content-Type':'text/html;charset=UTF-8',
    'Server ':'Apache-Coyote/1.1'
    'Set-Cookie':'COUNTRY_MATCH=true; Domain=tw.shop.com; Path=/'
    
}

res_get = requests.get(url, headers =headers)