# -*-coding:utf8-*-

import requests
import json
import pymysql
import sys
import datetime
import time
import imp
from multiprocessing.dummy import Pool as ThreadPool

def datatime_to_timestamp(d):
    now = lambda: int(round(time.time() * 1000))
    return now()


urls = []

head = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://space.bilibili.com/1847943/',
    'Origin': 'http://space.bilibili.com',
    'Host': 'space.bilibili.com',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}

time1 = time.time()

for i in range(1, 10):
    url = 'http://space.bilibili.com/ajax/member/GetInfo?mid=' + str(i)
    urls.append(url)

proxies = {

}

def getsources(url):
    payload = {
        '_': datatime_to_timestamp(datetime.datetime.now()),
        'mid': url.replace('http://space.bilibili.com/ajax/member/GetInfo?mid=', '')
    }

    print(payload)

    jscontent = requests.post('http://space.bilibili.com/ajax/member/GetInfo', headers = head, data = payload).content
    print(jscontent)

    time2 = time.time()
    js_dict = json.loads(jscontent.decode('utf-8'))

    if js_dict['status'] == True:
        js_data = js_dict['data']
        mid = js_data['mid']
        name = js_data['name']
        sex = js_data['sex']
        face = js_data['face']
        coins = js_data['coins']
        regtime = js_data['regtime']
        spacesta = js_data['spacesta']
        birthday = js_data['birthday']
        place = js_data['place']
        description = js_data['description']
        article = js_data['article']
        fans = js_data['fans']
        friend = js_data['friend']
        attention = js_data['attention']
        sign = js_data['sign']
        attentions = js_data['attentions']
        level = js_data['level_info']['current_level']
        exp = js_data['level_info']['current_exp']

        regtime_format = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(regtime))
        print("Succeed:" + mid + "\t" + str(time2 - time1))
        try:
            conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, db='bilibili')
            cur = conn.cursor()
            cur.execute('insert into user values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        [mid, name, sex, face, coins, regtime_format, spacesta, birthday, place, description,
                         article, fans, friend, attention, sign, str(attentions), level, exp])
            conn.commit()
            cur.close()
            conn.close()
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    else:
        print("Error: " + url)

pool = ThreadPool(10)
try:
    results = pool.map(getsources, urls)
except Exception:
    print("Connection Error")
    time.sleep(300)
    results = pool.map(getsources,urls)

pool.close()
pool.join()
