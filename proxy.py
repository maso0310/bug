from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

ua = UserAgent() # From here we generate a random user agent 從這裡我們生成一個隨機用戶代理
proxies = [] #Will contain proxies [ip, port]  將包含代理[ip，port]

# Main function
#主程式
def main():
  #Retrieve latest proxies
  #檢視最新的代理
  proxies_req = Request('https://www.sslproxies.org/')
  proxies_req.add_header('User-Agent', ua.random)
  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_doc, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')

  #Save proxies in the array
  #將代理存在陣列裡面
  for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })

  #Choose a random proxy
  #選擇一個隨機代理
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

  for n in range(1, 100):
    req = Request('http://icanhazip.com')
    req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

    # Every 10 requests, generate a new proxy
    #每十次的request產生一個代理
    if n % 3 == 0:
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

    # Make the call
    #製造一個呼叫
    try:
      my_ip = urlopen(req).read().decode('utf8')
      print('#' + str(n) + ': ' + my_ip)
    except: # If error, delete this proxy and find another one
      del proxies[proxy_index]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

# Retrieve a random index proxy (we need the index to delete it if not working)
#檢索隨機索引代理（如果不工作，我們需要索引刪除它）
def random_proxy():
  return random.randint(0, len(proxies) - 1)

if __name__ == '__main__':
  main()