#  爬取城市及uid信息，存入mysql

import requests
import json
import pymysql
import random
import time
from fake_headers import get_agent

db = pymysql.connect('localhost', 'root', 'password', 'baidumap')
cursor = db.cursor()

def getjson(loc, page_num):
    headers = get_agent()
    pa = {
        'query': '公园',
        'region': loc,
        'scope': '2',
        'page_size': 20,
        'page_num': page_num,
        'output': 'json',
        'ak': 'Gy7Hmmp2qCLg3T885tYGDpxFHcueom0P'
    }
    link = 'http://api.map.baidu.com/place/v2/search'
    r = requests.get(link, params=pa, headers=headers)
    decodejson = json.loads(r.text)
    time.sleep(1)
    return decodejson

city_list = []
with open(r"D:\Code\Python\WebScraping\BaiduMapAPI\cities.txt", 'r', encoding='utf-8') as txt_file:   
    for eachline in txt_file:
        city = list(filter(lambda ch: ch not in '\t\n0123456789', eachline))
        city = ''.join(city)
        city_list.append(city)

scrap_times = 0
for eachcity in city_list:
    not_last_page = True
    page_num = 0
    while not_last_page:
        decodejson = getjson(eachcity, page_num)
        print(eachcity, page_num)
        if decodejson['results']:
            for eachone in decodejson['results']:
                try:
                    park = eachone['name']
                except:
                    park = None
                try:
                    location_lat = eachone['location']['lat']
                except:
                    location_lat = None
                try:
                    location_lng = eachone['location']['lng']
                except:
                    location_lng = None
                try:
                    address = eachone['address']
                except:
                    address = None
                try:
                    street_id = eachone['street_id']
                except:
                    street_id = None
                try:
                    uid = eachone['uid']
                except:
                    uid = None
                sql = """INSERT INTO baidumap.city(city, park, location_lat, location_lng, address, street_id, uid)
                         Values(%s, %s, %s, %s, %s, %s, %s);"""
                cursor.execute(sql, (eachcity, park, location_lat, location_lng, address, street_id, uid))
                db.commit()
            page_num += 1
            scrap_times += 1
            if scrap_times % 10 == 0:
                sleep_time = random.randint(5, 10) + random.random()
            else:
                sleep_time = random.randint(0, 2) + random.random()
            time.sleep(sleep_time)
            print(f"开始休息：{sleep_time}秒")
        else:
            not_last_page = False
cursor.close()
db.close


    