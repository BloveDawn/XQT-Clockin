# Author: Blovedawn
# Date: 2021/07/19

import os
from sys import path as global_str_current_path
from time import strftime, localtime, sleep
from random import randint, shuffle
from json import loads as JsonLoads
from re import split as SplitString
from threading import Thread, active_count, Lock
from requests import post as RequestPost # pip install requests
from fake_useragent import UserAgent # pip install fake_useragent
from SendMail import SendEmail
from Config import *
from Const import *

GLOBAL_STR_CLOCKIN_URL = "http://yx.ty-ke.com/Home/Monitor/monitor_add" # clock in URL
GLOBAL_LIST_TASK = []
GLOBAL_LIST_ERROR_INFO = []
GLOBAL_LIST_EMAIL_ATTACH_PATH = []

class Clockin():
    
    # person info
    _str_person_info = None
    _str_person_id = None
    _str_person_address = None
    _str_person_remarks = None
    
    # post data
    _dict_request_header = {'User-Agent': ''}
    _dict_request_data = {
    'mobile': '', # actually this field is the person id
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
    
    # other
    _str_clockin_time = None
    _str_output_log_file_name = None
    _str_thread_name = None
    
    # is success
    _b_is_success = False
    
    def __init__(self, str_person_info_in:str, str_thread_name_in:str) -> None:
        # init param
        self._str_clockin_time = strftime("%Y-%m-%d-%H-%M-%S", localtime())
        self._str_thread_name = str_thread_name_in
        
        if len(str_person_info_in) <= 0:
            raise Exception('[-] [' + self._str_thread_name + '] [' + __name__ + ']  clockin init error: person info is empty string.')
        list_person_info = str_person_info_in.split(':') # split info line with ':'
        self._str_person_id = list_person_info[0] # get person id
        self._str_person_address = list_person_info[1] # get person address
        if len(self._str_person_id) <= 0 or len(self._str_person_address) <= 0:
            raise Exception('[-] [' + self._str_thread_name + '] [' + __name__ + ']  clockin init error: split args has empty string.')
        
        self._str_person_remarks = list_person_info[2] # get person remarks
        if len(self._str_person_remarks) <= 0:
            self._str_person_remarks = STR_DEFAULT_PERSON_REMARKS
        
        self._str_output_log_file_name = global_str_current_path[0] + '/' + STR_DEFAULT_SAVE_LOG_FOLDER_NAME + '/' + self._str_clockin_time + '_' + self._str_person_remarks + '.log' # log file path
        self.write_log_print('[!] [' + self._str_thread_name + '] [' + __name__ + '] time: ' + self._str_clockin_time)
        
        try:
            self._dict_request_header['User-Agent'] = UserAgent(use_cache_server=False).random # get a random user-agent
        except Exception:
            self._dict_request_header['User-Agent'] = STR_DEFAULT_USERAGENT # default ua
        
        self._dict_request_data['title'] += str(randint(0, 8)) # random temperature from 36.0 to 36.8
        self._dict_request_data['mobile'] = self._str_person_id
        if len(self._dict_request_data['mobile']) != 18:
            self.write_log_print_raise('[-] [' + self._str_thread_name + '] [' + __name__ + '] error: person id is not 18.')
            
        # address
        try:
            list_address = SplitString('[省市]', self._str_person_address)
            self._dict_request_data['address'] = self._str_person_address
        except:
            list_address = SplitString('[省市]', STR_DEFAULT_ADDRESS)
            self._dict_request_data['address'] = STR_DEFAULT_ADDRESS
        self._dict_request_data['province'] = list_address[0] + '省'
        self._dict_request_data['city'] = list_address[1] + '市'
        self._dict_request_data['district'] = list_address[2]
        self.write_log('[+] init success.')
    
    def run_clockin(self) -> bool:
        self.write_log_print('[!] [' + self._str_thread_name + '] [' + __name__ + '] person_remarks:' + self._str_person_remarks + ', person_id:' + self._str_person_id + ', person_address:' + self._str_person_address)
        try:
            if(DEBUG_ENABLED):
                str_response_text = open('debug_response.txt').read()
            else:
                str_response_text = RequestPost(url=GLOBAL_STR_CLOCKIN_URL, data=self._dict_request_data, headers=self._dict_request_header).text
            response_json_data = JsonLoads(str_response_text)
        except Exception as e:
            self.write_log('[!] response origin data: ' + str(str_response_text))
            self.write_log_print_raise('[-] [' + self._str_thread_name + '] [' + __name__ + '] request or load server response error: ' + str(e))
        response_code = response_json_data['code']
        response_msg = response_json_data['msg']
        # print info to log file
        if response_code == '200':
            self.write_log('[+] success 200')
        else:
            self.write_log('[-] error code: ' + str(response_code))
        self.write_log('[!] message: ' + str(response_msg))
        self.write_log('[!] request post URL: ' + str(GLOBAL_STR_CLOCKIN_URL))
        self.write_log('[!] request post data: ' + str(self._dict_request_data))
        self.write_log('[!] request head data: ' + str(self._dict_request_header))
        self.write_log('[!] response json data: ' + str(response_json_data))
        if response_code != '200':
            self.write_log_print_raise('[-] server error code: ' + response_code + ', time:' + self._str_clockin_time + ', person remarks:' + self._str_person_remarks + ', person id:' + self._str_person_id)
        self._b_is_success = True
        return self._b_is_success
        
    def write_log(self, str_in:str) -> None:
        f_logfile = open(self._str_output_log_file_name , 'a+')
        f_logfile.write(str_in + '\n')
        f_logfile.flush()
        f_logfile.close()
        
    def write_log_print(self, str_in:str) -> None:
        print(str_in)
        self.write_log(str_in)
    
    def write_log_print_raise(self, str_in:str) -> None:
        self.write_log_print(str_in)
        raise Exception(str_in)
        
    def get_failed_log_file_path(self):
        if not self._b_is_success:
            return self._str_output_log_file_name
        else:
            return None

GLOBAL_THREAD_LOCK = Lock()

class RunThread(Thread):
    _list_person_info = None
    
    def __init__(self, str_thread_name_in, list_person_info_in) -> None:
        super(RunThread, self).__init__(name=str_thread_name_in)
        self._list_person_info = list_person_info_in
        
    def run(self) -> None:
        print('[T] thread started: ' + self.name)
        for str_person_info in self._list_person_info:
            print('[T] [thread: ' + self.name + '] [' +__name__ + '] clockin info:' + str_person_info)
            sleep(randint(3, 15)) # clock in random 0-20 seconds
            GLOBAL_THREAD_LOCK.acquire(True) # lock
            clock_in_obj = Clockin(str_person_info, self.name)
            b_success = False
            try:
                b_success = clock_in_obj.run_clockin()
            except Exception as e:
                if DEBUG_ENABLED: print('[D] debug: ' + str(b_success)) # debug
                str_log_path = clock_in_obj.get_failed_log_file_path()
                if str_log_path is not None:
                    GLOBAL_LIST_EMAIL_ATTACH_PATH.append(str_log_path)
                GLOBAL_LIST_ERROR_INFO.append(str(e))
            GLOBAL_THREAD_LOCK.release() # release lock

if __name__ == "__main__":
    print('[!] XQT Clockin v2.0 By blovedawn')
    print('[!] [' + __name__ + '] running time: ' + strftime("%Y-%m-%d-%H:%M:%S", localtime()))
    print('[!] [' + __name__ + '] script running path:' + global_str_current_path[0] + '/')
    
    # check log file folder
    log_folder_path = global_str_current_path[0] + '/' + STR_DEFAULT_SAVE_LOG_FOLDER_NAME + '/'
    if not os.path.exists(log_folder_path):
        print('[+] [' + __name__ + '] create log folder: ' + log_folder_path)
        os.mkdir(log_folder_path)
    
    # get list_person_info from file STR_DEFAULT_SAVE_ID_FILE_NAME
    try:
        list_person_info = open(global_str_current_path[0] + '/' + STR_DEFAULT_SAVE_ID_FILE_NAME, 'r').read().splitlines()
        if len(list_person_info) == 0:
            str_error_list_empty = '[-] [' + __name__ + '] read person id list file ' + STR_DEFAULT_SAVE_ID_FILE_NAME + ' error, file is empty!'
            GLOBAL_LIST_ERROR_INFO.append(str_error_list_empty)
            print(str_error_list_empty)
            exit()
    except Exception as e:
        str_error_file_error = '[-] [' + __name__ + '] read id list file ' + STR_DEFAULT_SAVE_ID_FILE_NAME + ' error: ' + str(e)
        GLOBAL_LIST_ERROR_INFO.append(str_error_file_error)
        print(str_error_file_error)
        exit()

    # random and re-group person list
    shuffle(list_person_info)
    list_person_info_grouped = []
    for i in range(0, len(list_person_info), INT_PERSON_GROUP_COUNT):
        list_person_info_grouped.append(list_person_info[i:i+INT_PERSON_GROUP_COUNT])
    
    # run multi thread
    for list_person_info in list_person_info_grouped:
        RunThread(strftime("%Y-%m-%d-%H:%M:%S", localtime()), list_person_info).start()
        sleep(randint(3, 5))
    while(active_count() > 1): # wait for all sub threads
        print('[!] [' + __name__ + '] waiting ' + str(active_count()) + ' sub threads...')
        sleep(5)
    
    # email send error info
    if EMAIL_ENABLED:
        if len(GLOBAL_LIST_ERROR_INFO) != 0:
            STR_DEFAULT_EMAIL_TITLE = 'Please check errors when clock in XQT'
            STR_DEFAULT_EMAIL_CONTENT = '\n\n'.join(GLOBAL_LIST_ERROR_INFO) + '\n\n'
            email_send = SendEmail()
            email_send.set_args(email_to_in=EMAIL_RECEIVERS, email_cc_in=EMAIL_CC, email_bcc_in=EMAIL_BCC, email_title_in=STR_DEFAULT_EMAIL_TITLE, email_content_in=STR_DEFAULT_EMAIL_CONTENT, email_attach_path_in=GLOBAL_LIST_EMAIL_ATTACH_PATH)
            email_send.send_email()