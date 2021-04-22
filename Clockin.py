import random
import requests
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

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 5G Build/QKQ1.191222.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 Mobads'
}

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
    DATA['title'] = '36.' + str(random.randint(0, 8))
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
    page = requests.post(url=URL, data=DATA, headers=HEADER)
    code = json.loads(page.text)['code']
    msg = json.loads(page.text)['msg']
    
    # Print info to log file
    if code == '400':
        log_file.write('[-] Error 400\n')
        log_file.write('[-]')
    elif code == '200':
        log_file.write('[+] Success 200\n')
        log_file.write('[+]')
    else:
        log_file.write('[-] Unknow Error\n')
        log_file.write('[-]')
    log_file.write(' Msg:' + str(msg) + '\n')
    
    log_file.write('[!] URL:' + str(URL) + '\n')
    log_file.write('[!] DATA:' + str(DATA) + '\n')
    log_file.write('[!] HEAD:' + str(HEADER) + '\n')
    log_file.write('[!] RetData:' + str(page.text) + '\n')

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
        time.sleep(20) # clock in every 20 seconds