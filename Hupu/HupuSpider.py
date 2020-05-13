'''
import requests
from bs4 import BeautifulSoup
import datetime
from pymongo import MongoClient
'''
import time
from hupu_tools import get_data, get_page
from MongoAPI import MongoAPI

hupu_post = MongoAPI('localhost', 27017, 'hupu', 'post')
for i in range(1, 12):
    link = 'https://bbs.hupu.com/bxj-' + str(i)
    soup = get_page(link)

    post_all = soup.find('ul', class_='for-list')
    post_list = post_all.find_all('li')
    data_list = get_data(post_list)
    for each in data_list:
        hupu_post.update({'post_link': each[1]}, {'title': each[0],
                                                  'psot_link': each[1],
                                                  'author': each[2],
                                                  'author_page': each[3],
                                                  'start_date': each[4],
                                                  'reply': each[5],
                                                  'view': each[6],
                                                  'last_reply': each[7],
                                                  'last_reply_time': each[8]})
    time.sleep(3)
    print(f"第{i}页获取完成， 休息3秒！")
    