# 获取所有拥有公园的城市

import json
import time
import random
import requests


def getjson(loc, page_num=0):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    pa = {
        'query': '公园',
        'region': loc,
        'scope': '2',
        'page_size': 20,
        'page_num': page_num,
        'output': 'json',
        'ak': 'LOVdpnL0reRGKksCmGqlnccz4AbH8uCH'
    }
    link = 'http://api.map.baidu.com/place/v2/search'
    r = requests.get(link, params=pa, headers=headers)
    decodejson = json.loads(r.text)
    return decodejson

province_list = ['江苏省', '浙江省', '广东省', '福建省', '山东省', '河南省', '河北省', '四川省', '辽宁省', '云南省',
                 '湖南省', '湖北省', '江西省', '安徽省', '山西省', '广西壮族自治区', '陕西省', '黑龙江省', '内蒙古自治区',
                 '贵州省', '吉林省', '甘肃省', '新疆维吾尔自治区', '海南省', '宁夏回族自治区', '青海省', '西藏自治区']

for eachprovince in province_list:
    decodejson = getjson(eachprovince)
    random_time = random.randint(2, 5) + random.random()
    time.sleep(random_time)
    for eachcity in decodejson['results']:
        city = eachcity['name']
        num = eachcity['num']
        output = '\t'.join([city, str(num)]) + '\r\n'
        with open('cities.txt', 'a+', encoding='UTF-8', newline='') as f:
            f.write(output)

#  直辖市与港澳台地区需要单独获取
def getjson(loc, page_num=0):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    pa = {
        'query': '公园',
        'region': loc,
        'scope': '2',
        'page_size': 20,
        'page_num': page_num,
        'output': 'json',
        'ak': 'LOVdpnL0reRGKksCmGqlnccz4AbH8uCH'
    }
    link = 'http://api.map.baidu.com/place/v2/search'
    r = requests.get(link, params=pa, headers=headers)
    decodejson = json.loads(r.text)
    return decodejson

decodejson = getjson('全国')
six_cities_list = ['北京市', '上海市', '重庆市', '天津市', '香港特别行政区', '澳门特别行政区']
for eachprovince in decodejson['results']:
    city = eachprovince['name']
    num = eachprovince['num']  # 可以不保存num信息，或者通过filter.py去除num
    if city in six_cities_list:
        output = '\t'.join([city, str(num)]) + '\r\n'
        with open('cities.txt', 'a+', encoding='UTF-8',  newline='') as f:
            f.write(output)