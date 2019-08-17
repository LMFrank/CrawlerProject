# 异步爬取链家网信息

import asyncio
import aiohttp
import math
from lxml import etree
import pandas
import time
import re
import requests

location_info = '''    1-->南京
    2-->上海
    3-->北京
    按ENTER确认：'''
location_select = input(location_info)
location_dic = {
    '1': 'nj',
    '2': 'sh',
    '3': 'bj'
}
city_url = f'https://{location_dic[location_select]}.lianjia.com/ershoufang/'
down = input("请输入价格下限（万）：")
up = input("请输入价格上限（万）：")

inter_list = [(int(down), int(up))]
def binary(inter):
    lower = inter[0]
    upper = inter[1]
    ave = int((upper - lower) / 2)
    inter_list.remove(inter)
    print("已经缩小价格区间：", inter)
    inter_list.append((lower, lower+ave))
    inter_list.append((lower+ave, upper))

pagenum = {}
headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
def get_num(inter):
    link = city_url + f'bp{inter[0]}ep{inter[1]}/'
    r = requests.get(link, headers=headers)
    num = int(etree.HTML(r.text).xpath("//h2[@class='total fl']/span/text()")[0].strip())
    pagenum[(inter[0], inter[1])] = num
    return num

totalnum = get_num(inter_list[0])

judge = True
while judge:
    a = [get_num(x)>3000 for x in inter_list]
    if True in a:
        judge = True
        for i in inter_list:
            if get_num(i) > 3000:
                binary(i)
    else:
        judge = False
print("价格区间缩小完毕！", inter_list)
print(f"一共有{totalnum}条房源信息")

url_list = []
url_list_failed = []
url_list_successed = []
url_list_duplicated = []

for i in inter_list:
    totalpage = math.ceil(pagenum[i]/30)
    for j in range(1, totalpage+1):
        url = city_url + f'pg{j}bp{i[0]}ep{i[1]}/'
        url_list.append(url)
print("url列表获取完毕")

async def get_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, timeout=20) as resp:
            if resp.status == 200:
                url_list_successed.append(url)
            else:
                url_list_failed.append(url)
            result = await resp.text()
            return result

info_list = []
def get_info(detail):
    house_list = etree.HTML(detail).xpath('//ul[@class="sellListContent"]/li')
    print(f'开始抓取第{url_list.index(url)}个页面的数据,共计{len(url_list)}个页面')
    info_dict = {}
    index = 1
    print("开始抓取，", url)
    for house in house_list:
        try:
            info_dict['房屋名称'] = house.xpath('.//div[@class="title"]/a/text()')[0]            
        except:
            info_dict['房屋名称'] = 'None'
        try:
            info_dict['链接'] = house.xpath('.//div[@class="title"]/a/@href')[0]  
        except:
            info_dict['链接'] = 'None'
        try:
            sentence = house.xpath('.//div[@class="houseInfo"]')[0].xpath('string(.)').replace(' ', '')
            info_dict['小区'] = sentence.split('|')[0]
        except:
            info_dict['小区'] = 'None'
        try:
            info_dict['户型'] = sentence.split('|')[1]
        except:
            info_dict['户型'] = 'None'
        try:
            info_dict['面积'] = sentence.split('|')[2]
        except:
            info_dict['面积'] = 'None'
        try:
            info_dict['朝向'] = sentence.split('|')[3]
        except:
            info_dict['朝向'] = 'None'
        try:
            info_dict['装修'] = sentence.split('|')[4]
        except:
            info_dict['装修'] = 'None'
        try:
            info_dict['楼层'] = ''.join(house.xpath('.//div[@class="positionInfo"]/text()')[0].strip().replace(' ', '').split('-')[0])
        except:
            info_dict['楼层'] = 'None'
        try:
            info_dict['建造时间'] = ''.join(re.findall('\)(.*?)年', house.xpath('.//div[@class="positionInfo"]/text()')[0].strip()))
        except:
            info_dict['建造时间'] = 'None'
        try:
            info_dict['关注人数'] = ''.join(re.findall('[0-9]', house.xpath('.//div[@class="followInfo"]/text()')[0].strip().split('/')[0]))
        except:
            info_dict['关注人数'] = 'None' 
        try:
            info_dict['发布时间'] = house.xpath('.//div[@class="followInfo"]/text()')[0].strip().split('/')[1].replace(' ', '')
        except:
            info_dict['发布时间'] = 'None'
        try:
            info_dict['总价（万）'] = house.xpath('.//div[@class="totalPrice"]/span/text()')[0]
        except:
            info_dict['总价（万）'] = 'None'
        try:
            info_dict['均价（元/平米）'] = ''.join(re.findall('[0-9]', house.xpath('.//div[@class="unitPrice"]/span/text()')[0]))
        except:
            info_dict['均价（元/平米）'] = 'None'
        if True in [info_dict['链接'] in dic.values() for dic in info_list]:
            url_list_duplicated.append(info_dict)
        else:
            info_list.append(info_dict)
            url_list_successed.append(info_dict)
        print(f"第{index}条:    {info_dict['房屋名称']}→房屋信息抓取完毕！")
        index += 1
        info_dict = {}

async def handle_detail(url):
    detail = await get_html(url)
    for url in url_list:
        get_info(detail)

start = time.time()
tasks = [asyncio.ensure_future(handle_detail(url)) for url in url_list]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

url_list_unrequested = []
for url in url_list:
    if url not in url_list_successed or url_list_failed:
        url_list_unrequested.append(url)
while url_list_unrequested:
    tasks_unrequested = [asyncio.ensure_future(handle_detail(url)) for url in url_list_unrequested]
    loop.run_until_complete(asyncio.wait(tasks_unrequested))
    url_lst_unrequested = []
    for url in url_list:
        if url not in url_list_successed:
            url_lst_unrequested.append(url)

end = time.time()
print(f'当前价格区间段内共有{totalnum}套二手房源,(包含{len(url_list_duplicated)}条重复房源),实际获得{len(info_list)}条房源信息。')
print(f'总共耗时{end-start}秒')

df = pandas.DataFrame(info_list)
df.to_csv("test.csv", mode='a+', encoding='utf-8-sig')
