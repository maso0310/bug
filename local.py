import requests

def images():
    url = 'http://140.113.238.34:8000/'
    files = {'images': open('RIMG0424.JPG', 'rb')}
    multiple_files = [
        ('images', ('11.png', open('11.png', 'rb'), 'image/png')),
        ('images', ('desktop.png', open('desktop.png', 'rb'), 'image/png'))
    ]
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type':'multipart/form-data',
        'Cookie':'csrftoken=5ppAPfeyrYrRZFLkYjjZXY5NwZ0LRXrL',
        'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding':'gzip, deflate',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    # r = requests.post(url, files=multiple_files, headers=headers)
    r = requests.post(url, files=files, headers=headers)
    print(r.text)