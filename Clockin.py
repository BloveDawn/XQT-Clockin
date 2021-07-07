# Author: Blovedawn
# Release Date: 2021.6

import os
from random import randint
from json import loads as JsonLoads
from time import strftime, localtime, sleep
from sys import path as current_path
from re import split as SplitString
from requests import post as RequestPost # pip install requests
from fake_useragent import UserAgent # pip install fake_useragent

CLOCKIN_URL = "http://yx.ty-ke.com/Home/Monitor/monitor_add" # clock in URL

DEFAULT_STR = {
    'SAVE_ID_FILE_NAME': 'id_save.txt', # save id to this file
    'SAVE_LOG_FOLDER_NAME': 'ClockinLogArchive', # save log to this folder
    'ADDRESS': '山西省某市某地址', # default clockin address
    'USERAGENT': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 5G Build/QKQ1.191222.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36 Mobads', # default user-agent
}

def Clockin(in_person_id:str, in_person_address:str):
    
    # data field
    request_header = {'User-Agent': ''}
    request_data = {
    'mobile': '', # actually this field is the ID number
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
    
    # parameters check
    if len(in_person_id) == 0:
        return
    if len(in_person_address) == 0:
        in_person_address = DEFAULT_STR.get('ADDRESS')
    
    # initialize log write
    log_folder_path = current_path[0] + '/' + DEFAULT_STR.get('SAVE_LOG_FOLDER_NAME') + '/'
    if not os.path.exists(log_folder_path):
        os.mkdir(log_folder_path)
    log_file = open(log_folder_path + strftime("%Y-%m-%d-%H-%M-%S", localtime()) + '_' + in_person_id + '.log', 'w+')
    log_file.write('[!] time:' + strftime("%Y-%m-%d-%H-%M-%S", localtime()) + '\n')
    
    # input field
    request_header['User-Agent'] = UserAgent().random # get a random user-agent
    if request_header['User-Agent'] == '' or None: # default ua
        request_header['User-Agent'] = DEFAULT_STR.get('USERAGENT')
    
    request_data['title'] += str(randint(0, 8)) # random temperature from 36.0 to 36.8
    request_data['mobile'] = in_person_id
    
    if request_data['mobile'] == '':
        log_file.write('[-] error, person id is empty\n')
        return
    elif len(request_data['mobile']) != 18:
        log_file.write('[-] error, person id is not 18\n')
        return

    request_data['address'] = in_person_address
    
    address_list = SplitString('[省市]', in_person_address)
    if len(address_list) != 3:
        log_file.write('[-] error address list:' + str(address_list) + '\n')
        return
    
    request_data['province'] = address_list[0] + '省'
    request_data['city'] = address_list[1] + '市'
    request_data['district'] = address_list[2]
    
    # post to URL
    response_page = RequestPost(url=CLOCKIN_URL, data=request_data, headers=request_header).text
    try: # try to load response json
        response_json_data = JsonLoads(response_page)
    except Exception as e:
        print('[-] [' + __name__ + '] runtime error: ' + str(e) + '\n[-] time:' + strftime("%Y-%m-%d-%H-%M-%S", localtime()) + ' person_id:' + in_person_id + ', addr:' + in_person_address)
        log_file.write('[-] json load error: ' + str(e) + '\n')
        log_file.write('[!] original response page text:\n' + response_page + '\n')
        log_file.flush()
        log_file.close()
        print('[-] [' + __name__ + '] clockin server return error! person_id:' + in_person_id)
        return
    response_code = response_json_data['code']
    response_msg = response_json_data['msg']
    
    # print info to log file
    if response_code == '400':
        log_file.write('[-] error 400\n')
        log_file.write('[-]')
    elif response_code == '200':
        log_file.write('[+] success 200\n')
        log_file.write('[+]')
    else:
        log_file.write('[-] unknow error code:' + str(response_code) + '\n')
        log_file.write('[-]')
    log_file.write(' message: ' + str(response_msg) + '\n')
    
    log_file.write('[!] request post URL: ' + str(CLOCKIN_URL) + '\n')
    log_file.write('[!] request post data: ' + str(request_data) + '\n')
    log_file.write('[!] request head data: ' + str(request_header) + '\n')
    log_file.write('[!] response data: ' + str(response_json_data) + '\n')
    
    # release log file
    log_file.flush()
    log_file.close()

if __name__ == "__main__":
    # get current path
    script_run_path = current_path[0] + '/'
    print('[+] [' + __name__ + '] script running path:' + script_run_path)
    
    # log running time
    print('[!] running time:' + strftime("%Y-%m-%d-%H-%M-%S", localtime()))
    
    # get person_id_list from file DEFAULT_STR['SAVE_ID_FILE_NAME']
    try:
        person_id_list = open(script_run_path + DEFAULT_STR.get('SAVE_ID_FILE_NAME'), 'r').read().splitlines()
        if len(person_id_list) == 0:
            print('[-] [' + __name__ + '] read person id list file ' + DEFAULT_STR.get('SAVE_ID_FILE_NAME') + ' error, file is empty!')
            exit()
    except Exception as e:
        print('[-] [' + __name__ + '] read id list file ' + DEFAULT_STR.get('SAVE_ID_FILE_NAME') + ' error: ' + str(e))
        exit()
    
    # clock in
    for person_id in person_id_list:
        sleep(randint(0, 20)) # clock in every 0-20 seconds
        try:
            info_list = person_id.split(':') # split list with ':'
        except Exception as e_split:
            print('[-] [' + __name__ + '] split id error:' + str(e_split))
            continue
        print('[+] [' + __name__ + '] clockin id:' + info_list[0] + ', addr:' + info_list[1])
        try:
            Clockin(info_list[0], info_list[1])
        except Exception as e:
            print('[-] [' + __name__ + '] clockin func error! clockin ID:' + info_list[0] + ', addr:' + info_list[1])
        print('')
    exit()