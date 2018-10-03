import requests
from bs4 import BeautifulSoup

url = 'https://www.ifreesite.com/upload/imgur.php'

files = {'myfile':open('C:/bug/static/tmp/test.jpg','rb')}
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Content-Type':'multipart/form-data',
    'authority':'www.ifreesite.com',
    'Cookie':'__cfduid=de4e877e693f89857d7ccf5d3bacf09061538366301; _ga=GA1.2.70463292.1538366305; _gid=GA1.2.663308162.1538366305; __gads=ID=150ea221222963b2:T=1538443603:S=ALNI_MbatGMuvObwP1ekOfnifQOafX_hzQ'
}

post = requests.post(url, headers=headers,files=files,data = {'submit':'上傳圖片'})
soup_post = BeautifulSoup(post.text,'html.parser')
outcome = soup_post.find('p')
print(post.status_code)
print(post)
print(outcome)
print(soup_post)