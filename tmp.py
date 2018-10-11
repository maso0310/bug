import requests
import time

urls = 'http://140.113.238.34:8000/'

for url in urls:
    for i in range(10):
        try:
            r = requests.get(url).content
        except Exception as e:
            if i >= 9:
                do_some_log()
            else:
                time.sleep(0.5)
        else:
            time.sleep(0.1)
            break

    print(r)