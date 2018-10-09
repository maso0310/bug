import requests


resp = requests.get("https://tw.shop.com")
print(resp.text.split())