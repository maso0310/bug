import requests
import random
from bs4 import BeautifulSoup  
  
url = 'http://140.113.238.34:8000/'


res_get = requests.get(url,timeout=3600)
soup_get = BeautifulSoup(res_get.text,'html.parser')
csrf_value = soup_get.find('input')['value']
print('csrftoken='+csrf_value)