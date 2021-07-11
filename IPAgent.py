from time import sleep
from random import choice
from requests import get as HttpGet
from bs4 import BeautifulSoup
from fake_useragent import UserAgent # pip install fake_useragent
from Const import *

class ProxyDataField():
    IP_ADDRESS = 0
    PORT = 1
    POSITION = 2
    PROXY_CLASS = 3
    CHECK_TIME = 4
    

class IPAgent:
    _webpage_path_base = ''
    _webpage_path = ''
    _proxy_list_origin = []
    _proxy_list  = []
    _request_header = {'User-Agent': ''}
    _proxies_header = { 'http': '', 'https': ''}
    
    def __init__(self) -> None:
        self._webpage_path_base = IPAGENT_URL
        
        # get proxy servers
        for i in range(1, 2):
            sleep(2)
            self.RandomUA()
            page_text = HttpGet(self._webpage_path_base + str(i) + '.html', headers=self._request_header).content.decode('GBK')
            bs4_page = BeautifulSoup(page_text, 'html.parser')
            rows = bs4_page.find_all('tr')
            for row in rows:
                row_str = row.text
                if 'ip' in row_str:
                    continue
                proxy_ip_address = str(row.contents[ProxyDataField.IP_ADDRESS].text)
                proxy_port = str(row.contents[ProxyDataField.PORT].text)
                self._proxy_list_origin.append(proxy_ip_address + ':' + proxy_port)
        print('[+] proxy get count:' + str(len(self._proxy_list_origin)))
        
        # split with :
        for proxy_origin in self._proxy_list_origin:
            each_list = []
            each_list.append(str(proxy_origin).split(':'))
            self._proxy_list.append(each_list)

        # test proxy
        print('[!] testing proxy...')
        if(self.TestProxy()):
            print('[+] proxy test ok')
        else:
            print('[-] proxy test error')
    
    def RandomUA(self):
        try:
            self._request_header['User-Agent'] = UserAgent(use_cache_server=False).random # get a random user-agent
            print('[+] proxy set random ua ok')
        except Exception:
            self._request_header['User-Agent'] = DEFAULT_STR.get('USERAGENT') # default ua
            print('[-] proxy set random ua error')
    
    def SetRandomProxy(self):
        random_proxy = choice(self._proxy_list)[0]
        self._proxies_header['http'] = 'http://' + random_proxy[ProxyDataField.IP_ADDRESS] + ':' + random_proxy[ProxyDataField.PORT]
        self._proxies_header['https'] = 'http://' + random_proxy[ProxyDataField.IP_ADDRESS] + ':' + random_proxy[ProxyDataField.PORT]
        print('[+] proxy set random ok: ' + self._proxies_header['http'])
        
    def TestProxy(self) -> bool:
        self.RandomUA()
        self.SetRandomProxy()
        
        try:
            page = HttpGet(url='https://ip.chinaz.com/', proxies=self._proxies_header, headers=self._request_header).text
            print(page)
            return True
        except Exception as e:
            print('[-] proxy return error: ' + str(e))
            return False
    
    def Get(self, get_path_in:str):
        pass

if __name__ == '__main__':
    test = IPAgent()