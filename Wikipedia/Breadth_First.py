# 广度优先的多线程爬虫

import threading
import requests
import re
import time

g_mutex = threading.Condition()
g_pages = []  # 存储广度爬虫获取的html代码，之后解析所有url链接
g_queueURL = []  # 等待爬取的url链接列表
g_existURL = []  # 已经爬取过的url链接列表
g_writecount = 0  # 找到的链接数

class Crawler(object):
    def __init__(self, url, threadnum):
        self.url = url
        self.threadnum = threadnum
        self.threadpool = []

    def craw(self):  # 爬虫的控制大脑，包括爬取网页，更新队列
        global g_queueURL
        g_queueURL.append(url)
        depth = 1
        while depth < 3:
            print("Searching depth", depth, "...\n")
            self.downloadAll()
            self.updateQueueURL()
            g_pages = []
            depth += 1
    
    def downloadAll(self):  # 调用多线程爬虫，在小于线程最大值和没爬完队列之前，会增加线程
        global g_queueURL
        i = 0
        while i < len(g_queueURL):
            j = 0
            while j < self.threadnum and i+j < len(g_queueURL):
                threadresult = self.download(g_queueURL[i+j], j)
                j += 1
            i += j
            for thread in self.threadpool:
                thread.join(30)
            threadpool = []
        g_queueURL = []
    
    def download(self, url, tid):  # 调用多线程爬虫
        crawthread = CrawlerThread(url, tid)
        self.threadpool.append(crawthread)
        crawthread.start()

    def updateQueueURL(self):  # 完成一个深度的爬虫之后，更新队列
        global g_queueURL
        global g_existURL
        newUrlList = []
        for content in g_pages:
            newUrlList += self.getUrl(content)
        g_queueURL = list(set(newUrlList) - set(g_existURL))

    def getUrl(self, content):  # 从获取的网页中解析url
        link_list = re.findall('<a href="/wiki/([^:#=<>]*?)".*?</a>', content)
        unique_list = list(set(link_list))
        return unique_list

class CrawlerThread(threading.Thread):  # 爬虫线程
    def __init__(self, url, tid):
        threading.Thread.__init__(self)
        self.url = url
        self.tid = tid
    
    def run(self):
        global g_mutex
        global g_writecount
        try:
            print(self.tid, 'crawl ', self.url)
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
            link = "https://en.wikipedia.org/wiki/" + self.url
            r = requests.get(link, headers=headers)
            html = r.text

            link_list2 = re.findall('<a href="/wiki/([^:#=<>]*?)".*?</a>', html)
            unique_list2 = list(set(link_list2))
            for eachone in unique_list2:
                g_writecount += 1
                content2 = ('No.' + str(g_writecount) + '\t Thread' + str(self.tid) + '\t' + self.url + '->' + eachone + '\n')
                with open(r'D:\Code\Python\WebScraping\Wikipedia\link_14_4.txt'
                          , 'a+') as f:
                    f.write(content2)
        except Exception as e:
            g_mutex.acquire()
            g_existURL.append(self.url)
            g_mutex.release()
            print("Failed downloading and saving", self.url)
            print(e)
            return None
        g_mutex.acquire()
        g_pages.append(html)
        g_existURL.append(self.url)
        g_mutex.release()

if __name__ == '__main__':
    url = 'Wikipedia'
    threadnum = 10
    crawler = Crawler(url, threadnum)
    start = time.time()
    crawler.craw()
    stop = time.time()
    print("广度优先的多线程爬虫所用时间为：", stop-start)
