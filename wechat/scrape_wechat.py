# -*- coding: utf-8 -*-

import requests
import json
import re
import random
import time
import codecs
from dateutil import parser
from json import dumps
from datetime import date, datetime

from collections import OrderedDict
from pymongo import MongoClient

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

url = 'https://mp.weixin.qq.com'
header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    }
 
f = codecs.open('cookie.txt', 'r', encoding='utf-8')
cookie = f.read()
cookies = json.loads(cookie)
response = requests.get(url=url, cookies=cookies)
token = re.findall(r'token=(\d+)', str(response.url))[0]
print("token = ", token)

query_id_data = {
    'token': token,
    'lang': 'zh_CN',
    'f': 'json',
    'ajax': '1',
    'random': random.random(),
    'action': 'list_ex',
    'begin': '0',
    'count': '10',
    'type': '10'
}
appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
max_num = appmsg_response.json().get('app_msg_cnt')

print("max_num = ", max_num)

#max_num = 10

num = int(int(max_num) / 10)
begin = 0

# insert into json file
file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

# setting for mongoDB
client = MongoClient('localhost', 27017)
db = client.importnewDb
wechat_posts = db.wechatPosts

result = wechat_posts.remove()
print('Cleaned mongodb Collections', result)

while num + 1 > 0 :
    query_id_data = {
	    'token': token,
	    'lang': 'zh_CN',
	    'f': 'json',
	    'ajax': '1',
	    'random': random.random(),
	    'action': 'list_ex',
	    'begin': '{}'.format(str(begin)),
	    'count': '10',
	    'type': '10'
	}
    print('next page###################', begin)
    query_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    items = query_response.json().get('app_msg_list')
    for item in items:
        trimmed_title = re.sub(r'\s+', '', item.get('title'))
        item['title'] = trimmed_title
        time_str = time.strftime('%Y%m%d', time.localtime(item.get('update_time')))
        item['update_date'] = int(time_str)
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        file.write(line)

        post_id = wechat_posts.insert_one(item).inserted_id
        #print("post_id = ", post_id)

    num -= 1
    begin = int(begin)
    begin += 10
    time.sleep(2)
