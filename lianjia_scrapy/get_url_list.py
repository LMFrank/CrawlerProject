import math
import requests
from lxml import etree

city_url = 'https://nj.lianjia.com/zufang/'
inter_list = [(1000, 2500)]
def binary(inter):
    lower = inter[0]
    upper = inter[1]
    ave = int((upper-lower)/2)
    inter_list.remove(inter)
    print("已经缩小价格区间：", inter)
    inter_list.append((lower, lower+ave))
    inter_list.append((lower+ave, upper))
    
pagenum = {}
headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
def get_num(inter):
    link = city_url + f'brp{inter[0]}erp{inter[1]}/'
    r = requests.get(link, headers=headers)
    num = int(etree.HTML(r.text).xpath('//p[@class="content__title"]/span/text()')[0])
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
with open(r'D:\Code\Python\CrawlerProjectCopy\lianjia_scrapy\url_list.txt', 'a+') as f:
    for i in inter_list:
        totalpage = math.ceil(pagenum[i]/30)
        for j in range(1, totalpage+1):
            url = city_url + f'pg{j}brp{i[0]}erp{i[1]}/'
            f.write(url + '\r')
    print("url列表获取完毕")

