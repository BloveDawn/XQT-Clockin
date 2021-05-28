import random
import requests
from fake_useragent import UserAgent
import json
import time
import sys
import os
import re

URL = "http://yx.ty-ke.com/Home/Monitor/monitor_add" # clock in URL

DATA = {
    'mobile': '', # Actually this field is the ID number
    'title': '36.', # temperature
    'jk_type': '健康',
    'wc_type': '否',
    'jc_type': '否',
    'province': '',
    'city': '',
    'district': '',
    'address': '',
    'is_verify': '0',
}

HEADER = {'User-Agent': ''}

def Clockin(id:str, address:str):
    # Parameters check
    if len(id) == 0:
        return
    if len(address) == 0:
        address = '山西省某市某地址'
    
    # Initialize log write
    print('[!] Timestamp:' + str(time.time()))
    log_folder_path = sys.path[0] + '/' + 'ClockinLogArchive/'
    if not os.path.exists(log_folder_path):
        os.mkdir(log_folder_path)
    log_file = open(log_folder_path + str(time.time()) + '_' + id + '.log', 'w+')
    log_file.write('[!] Timestamp:' + str(time.time()) + '\n')
    
    # Input field
    HEADER['User-Agent'] = UserAgent().random # random User-Agent
    if HEADER['User-Agent'] == '' or None: # default ua
        HEADER['User-Agent'] = 'Mozilla/5.0 (Linux; Android 10; Redmi K30 5G Build/QKQ1.191222.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 Mobads'
    
    DATA['title'] = '36.' + str(random.randint(0, 8)) # temperature from 36.0 to 36.8
    DATA['mobile'] = id
    
    if DATA['mobile'] == '':
        log_file.write('[-] Error mobile empty\n')
        return
    elif len(DATA['mobile']) != 18:
        log_file.write('[-] Error mobile not 18\n')
        return

    DATA['address'] = address
    
    address_list = re.split('[省市]', address)
    if len(address_list) != 3:
        log_file.write('[-] Error address list:' + str(address_list) + '\n')
        return
    
    DATA['province'] = address_list[0] + '省'
    DATA['city'] = address_list[1] + '市'
    DATA['district'] = address_list[2]
    
    # Post to URL
    
    response_page = requests.post(url=URL, data=DATA, headers=HEADER).text
    try: # try to load response json
        response_json_data = json.loads(response_page)
    except Exception as e:
        log_file.write('[-] Json load error: ' + str(e) + '\n')
        log_file.write('[!] Original response page text:\n' + response_page + '\n')
        log_file.flush()
        log_file.close()
        print('[-] Clockin server return error! ID:' + id)
        return
    response_code = response_json_data['code']
    response_msg = response_json_data['msg']
    
    # Print info to log file
    if response_code == '400':
        log_file.write('[-] Error 400\n')
        log_file.write('[-]')
    elif response_code == '200':
        log_file.write('[+] Success 200\n')
        log_file.write('[+]')
    else:
        log_file.write('[-] Unknow Error Code:' + str(response_code) + '\n')
        log_file.write('[-]')
    log_file.write(' Message: ' + str(response_msg) + '\n')
    
    log_file.write('[!] Request post URL: ' + str(URL) + '\n')
    log_file.write('[!] Request post data: ' + str(DATA) + '\n')
    log_file.write('[!] Request head data: ' + str(HEADER) + '\n')
    log_file.write('[!] Response data: ' + str(response_json_data) + '\n')
    
    # release log file
    log_file.flush()
    log_file.close()

if __name__ == "__main__":
    # Get id list from file 'id_save.txt'
    id_list = []
    run_path = sys.path[0] + '/'
    print('[+] run_path:' + run_path)
    id_list = open(run_path + 'id_save.txt', 'r').read().splitlines()
    
    # Check is empty
    if len(id_list) == 0:
        exit(-1)
    
    # Clock in
    for id in id_list:
        info_list = id.split(':') # split list with ':'
        print('[+] Clockin ID:' + info_list[0] + ', Addr:' + info_list[1])
        try:
            Clockin(info_list[0], info_list[1])
        except Exception as e:
            print('[-] Clockin Error!')
            err_log = open(run_path + 'imp-error.log', 'a+')
            err_log.write('[-] Error ' + str(time.time()) + ':\n' + str(e) + '\n\n')
        time.sleep(15) # clock in every 15 seconds