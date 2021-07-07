# Author: Blovedawn
# Release Date: 2021.6

# Updated Date: 2021.7.7

import os
from random import randint, shuffle
from json import loads as JsonLoads
from time import strftime, localtime, sleep
from sys import path as current_path
from re import split as SplitString
from requests import post as RequestPost # pip install requests
from fake_useragent import UserAgent # pip install fake_useragent
from Const import *

def Clockin(person_id_in:str, person_address_in:str, person_remarks_in:str):
    
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
    if len(person_id_in) == 0:
        return
    if len(person_address_in) == 0:
        person_address_in = DEFAULT_STR.get('ADDRESS')
    if len(person_remarks_in) == 0:
        person_remarks_in = "Unknown"
    
    # initialize log write
    log_folder_path = current_path[0] + '/' + DEFAULT_STR.get('SAVE_LOG_FOLDER_NAME') + '/'
    if not os.path.exists(log_folder_path):
        os.mkdir(log_folder_path)
    log_file = open(log_folder_path + strftime("%Y-%m-%d-%H-%M-%S", localtime()) + '_' + person_remarks_in + '.log', 'w+')
    log_file.write('[!] time:' + strftime("%Y-%m-%d-%H-%M-%S", localtime()) + '\n')
    log_file.write('[!] person info: id:' + person_id_in + ', remarks:' + person_remarks_in + '\n')
    
    # input field
    ua = UserAgent(use_cache_server=False)
    request_header['User-Agent'] = ua.random # get a random user-agent
    if request_header['User-Agent'] == '' or None: # default ua
        request_header['User-Agent'] = DEFAULT_STR.get('USERAGENT')
    
    request_data['title'] += str(randint(0, 8)) # random temperature from 36.0 to 36.8
    request_data['mobile'] = person_id_in
    
    if request_data['mobile'] == '':
        log_file.write('[-] error, person id is empty\n')
        return
    elif len(request_data['mobile']) != 18:
        log_file.write('[-] error, person id is not 18\n')
        return

    request_data['address'] = person_address_in
    
    address_list = SplitString('[省市]', person_address_in)
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
        print('[-] [' + __name__ + '] runtime error: ' + str(e) + '\n[-] time:' + strftime("%Y-%m-%d-%H-%M-%S", localtime()) + ' person_id:' + person_id_in + ', addr:' + person_address_in + ', remarks:' + person_remarks_in)
        log_file.write('[-] json load error: ' + str(e) + '\n')
        log_file.write('[!] original response page text:\n' + response_page + '\n')
        log_file.flush()
        log_file.close()
        print('[-] [' + __name__ + '] clockin server return error! person_id:' + person_id_in + ', remarks:' + person_remarks_in)
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
        person_info_list = open(script_run_path + DEFAULT_STR.get('SAVE_ID_FILE_NAME'), 'r').read().splitlines()
        if len(person_info_list) == 0:
            print('[-] [' + __name__ + '] read person id list file ' + DEFAULT_STR.get('SAVE_ID_FILE_NAME') + ' error, file is empty!')
            exit()
    except Exception as e:
        print('[-] [' + __name__ + '] read id list file ' + DEFAULT_STR.get('SAVE_ID_FILE_NAME') + ' error: ' + str(e))
        exit()
    
    # random sort person info list
    shuffle(person_info_list)
    
    # clock in
    for person_info in person_info_list:
        sleep(randint(5, 25)) # clock in every 0-20 seconds
        try:
            person_info_list = person_info.split(':') # split info line with ':'
            person_id = person_info_list[0] # get person id
            person_address = person_info_list[1] # get person address
            person_remarks = person_info_list[2] # get person remarks
        except Exception as e_split:
            print('[-] [' + __name__ + '] split id error:' + str(e_split))
            continue
        print('[+] [' + __name__ + '] clockin id:' + person_id + ', addr:' + person_address + ', remarks:' + person_remarks)
        try:
            Clockin(person_id, person_address, person_remarks)
        except Exception as e:
            print('[-] [' + __name__ + '] clockin func error! clockin ID:' + person_id + ', addr:' + person_address + ', remarks:' + person_remarks)
    exit()