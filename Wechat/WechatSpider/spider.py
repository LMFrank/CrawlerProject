from requests import Session
from WechatSpider.config import *
from WechatSpider.db import RedisQueue
from WechatSpider.mysqlapi import MySQL
from WechatSpider.request import WechatRequest
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
from requests import ReadTimeout, ConnectionError

class Spider(object):
    base_url = 'http://weixin.sogou.com/weixin'
    keyword = 'iphone'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'cookies',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    session = Session()
    queue = RedisQueue()
    mysql = MySQL()

    def get_proxy(self):
        """
        从代理池获取代理
        :return:
        """
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                print('Get Proxy', response.text)
                return response.text
            return None
        except requests.ConnectionError:
            return None

    def start(self):
        """
        初始化工作
        """
        self.session.headers.update(self.headers)
        start_url = self.base_url + '?' + urlencode({'query': self.keyword, 'type': 2})
        wechat_request = WechatRequest(url=start_url, callback=self.parse_index, need_proxy=True)
        self.queue.add(wechat_request)

    def parse_index(self, response):
        """
        解析索引页
        :param response: 响应
        :return: 新的响应
        """
        doc = pq(response.text)
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            url = item.attr('href')
            wechat_request = WechatRequest(url=url, callback=self.parse_index, need_proxy=True)
            yield wechat_request
        next = doc('#sogou_next').attr('href')
        if next:
            url = self.base_url + str(next)
            wechat_request = WechatRequest(url=url, callback=self.parse_index, need_proxy=True)
            yield wechat_request

    def parse_detail(self, response):
        """
        解析页详情
        :param response: 响应
        :return: 微信公众号文章
        """
        doc = pq(response.text)
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#post-date').text(),
            'nickname': doc('#js_profile_qrcode div strong').text(),
            'wechat': doc('#js_profile_qrcode div p:nth-child(3) span').text()
        }
        yield data

    def request(self, wechat_request):
        """
        执行请求
        :param wechat_request: 请求
        :return: 响应
        """
        try:
            if wechat_request.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    proxies = {
                        'http': 'http://' +proxy,
                        'https': 'https://' +proxy
                    }
                    return self.session.send(wechat_request.prepare(), timeout=wechat_request.timeout, allow_redirects=True, proxies=proxies)
            return self.session.send(wechat_request.prepare(), timeout=wechat_request.timeout, allow_redirects=False)
        except (ConnectionError, ReadTimeout) as e:
            print('Error!', e.args)
            return False

    def error(self, wechat_request):
        """
        错误处理
        :param wechat_request: 请求
        :return:
        """
        wechat_request.fail_time = wechat_request.fail_time + 1
        print('Request Failed', wechat_request.fail_time, 'Times', wechat_request.url)
        if wechat_request.fail_time < MAX_FAILED_TIME:
            self.queue.add(wechat_request)

    def schedule(self):
        """
        调度请求
        :return:
        """
        while not self.queue.empty():
            wechat_request = self.queue.pop()
            callback = wechat_request.callback
            print('Schedule', wechat_request.url)
            response = self.request(wechat_request)
            if response and response.status_code in VALID_STATUSES:
                results = list(callback(response))
                if results:
                    for result in results:
                        print('New Result', type(result))
                        if isinstance(result, WechatRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            self.mysql.insert('articles', result)
                else:
                    self.error(wechat_request)
            else:
                self.error(wechat_request)

    def run(self):
        """
        入口
        :return:
        """
        self.start()
        self.schedule()

if __name__ == '__main__':
    spider = Spider()
    spider.run()