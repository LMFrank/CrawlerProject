#  从mysql获取之前爬取的uid通过百度地图api获得公园的详情

import requests
import json
import pymysql
import time
import random
from fake_headers import get_agent
#  from get_ip import get_ip_list, get_random_ip

db = pymysql.connect('localhost', 'root', 'password', 'baidumap')
cursor = db.cursor()
sql = """select city, uid from baidumap.city where id > 0;"""  # 发生错误时，更改id
cursor.execute(sql)
db.commit()
results = cursor.fetchall()

def getjson(uid):
    headers = get_agent()
    pa = {
        'uid': uid,
        'scope': '2',
        'output': 'json',
        'ak': 'Gy7Hmmp2qCLg3T885tYGDpxFHcueom0P'
    }
    link = 'http://api.map.baidu.com/place/v2/detail'
    r = requests.get(link, params=pa, headers=headers)

    '''
    if scrap_times % 200 == 0:
        ip_link = 'http://www.xicidaili.com/nn/'
        ip_list = get_ip_list(ip_link, headers=headers)
        proxies = get_random_ip(ip_list)
        r = requests.get(link, params=pa, headers=headers, proxies=proxies)
    else:
        r = requests.get(link, params=pa, headers=headers)
    '''

    decodejson = json.loads(r.text)
    #  time.sleep(1)
    return decodejson

scrap_times = 0
for row in results:
    city = row[0]
    uid = row[1]
    decodejson = getjson(uid)
    print(city, uid)
    info = decodejson['result']
    try:
        park = info['name']
    except:
        park = None
    try:
        city = info['city']
    except:
        city = row[0]
    try:
        location_lat = info['location']['lat']
    except:
        location_lat = None
    try:
        location_lng = info['location']['lng']
    except:
        location_lng = None
    try:
        address = info['address']
    except:
        address = None
    try:
        street_id = info['street_id']
    except:
        street_id = None
    try:
        uid = info['uid']
    except:
        uid = None
    try:
        telephone = info['telephone']
    except:
        telephone = None
    try:
        detail = info['detail']
    except:
        detail = None
    try:
        tag = info['detail_info']['tag']
    except:
        tag = None
    try:
        detail_url = info['detail_info']['detail_url']
    except:
        detail_url = None
    try:
        type = info['detail_info']['type']
    except:
        type = None
    try:
        price = info['detail_info']['price']
    except:
        price = None
    try:
        overall_rating = info['detail_info']['overall_rating']
    except:
        overall_rating = None
    try:
        image_num = info['detail_info']['image_num']
    except:
        image_num = None
    try:
        comment_num = info['detail_info']['comment_num']
    except:
        comment_num = None
    try:
        key_words = info['detail_info']['content_tag']
    except:
        key_words = None
    try:
        shop_hours = info['detail_info']['shop_hours']
    except:
        shop_hours = None            
    try:
        alias_list = info['detail_info']['alias']
        alias = ';'.join(alias_list)
    except:
        alias = None
    try:
        scope_type = info['detail_info']['scope_type']
    except:
        scope_type = None            
    try:
        scope_grade = info['detail_info']['scope_grade']
    except:
        scope_grade = None
    
    sql = """INSERT INTO baidumap.park
    (park, city, location_lat, location_lng, address, street_id, uid, telephone, detail, tag, detail_url, type, price, overall_rating, image_num, 
    comment_num, key_words, shop_hours, alias, scope_type, scope_grade)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    cursor.execute(sql, (park, city, location_lat, location_lng, address, street_id, uid, telephone, detail, tag, detail_url, 
                         type, price, overall_rating, image_num, comment_num, key_words, shop_hours, alias, scope_type, scope_grade))
    db.commit()
    scrap_times += 1
    if scrap_times % 100 == 0:
        sleep_time = random.randint(5, 10) + random.random()
        time.sleep(sleep_time)
        print(f"开始休息：{sleep_time}秒")
    elif scrap_times % 150 == 0:
        sleep_time = random.randint(11, 15) + random.random()
        time.sleep(sleep_time)
        print(f"开始休息：{sleep_time}秒")
    elif scrap_times % 900 == 0:
        sleep_time = random.randint(30, 35) + random.random()
        time.sleep(sleep_time)
        print(f"开始休息：{sleep_time}秒")
    else:
        sleep_time = random.randint(0, 1) + random.random()
    
cursor.close()
db.close                     