import requests
from bs4 import BeautifulSoup

url = 'http://140.113.238.34:8000/'
'''
resp = requests.get(url)
soup_get= BeautifulSoup(resp.text,'html5lib')
'''
files = 'IMAG1876.jpg'
headers = {
    'Referer':'http://140.113.238.34:8000/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Content-Type':'multipart/form-data',
    'Cookie':'csrftoken=5ppAPfeyrYrRZFLkYjjZXY5NwZ0LRXrL'
}
'''
form_data = {
    "csrfmiddlewaretoken":'5ppAPfeyrYrRZFLkYjjZXY5NwZ0LRXrL',
    "myfile":files
}
'''

post = requests.post(url, data = {'csrfmiddlewaretoken':'5ppAPfeyrYrRZFLkYjjZXY5NwZ0LRXrL'},headers=headers,files=files)
soup_post = BeautifulSoup(post.text,'html.parser')
outcome = soup_post.find('p')
print(post.text)