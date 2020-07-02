# -*- coding: utf-8 -*-
import requests
import re
import json

from pyquery import PyQuery as pq
from requests import RequestException


class Bilibili(object):
    def __init__(self):
        self.getHtmlHeaders={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9'
        }

        self.downloadVideoHeaders={
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/video/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36',
        }

    def get_html(self, url):
        try:
            response = requests.get(url=url, headers= self.getHtmlHeaders)
            print(response.status_code)
            if response.status_code == 200:
                return response.text
        except RequestException:
            print('请求Html错误: e')

    def parse_html(self, html):
        doc = pq(html)
        video_title = doc('#viewbox_report > h1 > span').text()

        pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
        result = re.findall(pattern, html)[0]
        temp = json.loads(result)
        video_url = temp['data']['dash']['video'][0]['baseUrl']
        return{
            'title': video_title,
            'url': video_url
        }

    def download_video(self,video):
        title = re.sub(r'[\/:*?"<>|]', '-', video['title'])
        url = video['url']
        filename = title +'.flv'
        with open(filename, "wb") as f:
            f.write(requests.get(url=url, headers=self.downloadVideoHeaders, stream=True, verify=False).content)

    def run(self, url):
        self.download_video(self.parse_html(self.get_html(url)))

if __name__ == '__main__':
    url = input("input url: ")
    Bilibili().run(url)