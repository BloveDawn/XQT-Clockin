from tempfile import gettempdir
from sys import path as current_path
from Const import FAKE_UA_CACHE_NAME

print("[!] current path:" + current_path[0] + '/' + FAKE_UA_CACHE_NAME)
print("[!] target path:" + gettempdir() + '/' + FAKE_UA_CACHE_NAME)

f_ua_cache = open(gettempdir() + '/' + FAKE_UA_CACHE_NAME, 'w+')
f_ua_cache.write(open(current_path[0] + '/' + FAKE_UA_CACHE_NAME).read())
f_ua_cache.flush()
f_ua_cache.close()
print('[!] copy cache file end.')