import requests
import random
from bs4 import BeautifulSoup

def post_image_to_url(path):
    url = 'http://pythonscraping.com/pages/files/processing2.php'

    res_get = requests.get(url)
    print(res_get)
    print(res_get.text)
    soup_get = BeautifulSoup(res_get.text,'html.parser')
    print(soup_get)
    #csrf_value = soup_get.find('input')['value']
    #print('csrftoken='+csrf_value)

    #data = {'csrfmiddlewaretoken':csrf_value} 
    files = {'myfile':open('/app/home/'+path,'rb')}

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer':'http://140.113.238.34:8000/',
        'host':'ricebug.herokuapp.com'
    #    'Cookie':'csrftoken='+csrf_value
    }

    res_post = requests.post(url,files=files,timeout=3600)
    print(res_post)
  #  soup_post = BeautifulSoup(res_post.text,'html.parser')
 #   outcome = soup_post.find_all('body')
#    print(outcome)
    bug_number = res_post.text
    print('request,done')
    return(bug_number)