# 深度优先的递归爬虫

import requests
import re
import time

exist_url = []
g_writecount = 0

def scrappy(url, depth=1):
    global g_writecount
    try:
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
                   AppleWebKit/537.36 (KHTML, like Gecko) 
                   Chrome/75.0.3770.142 Safari/537.36"
                   }
        url = 'https://en.wikipedia.org/wiki/' + url
        r = requests.get(url, headers=headers)
        html = r.text
    except Exception as e:
        print("Failed downloading and saving ", url)
        print(e)
        exist_url.append(url)
        return None
    
    exist_url.append(url)
    # 去除不需要的url链接（侧边栏、页眉等）url链接以/wiki/开头，且不包含:#=<>
    link_list = re.findall('<a href="/wiki/([^:#=<>]*?)".*?</a>', html)
    unique_list = list(set(link_list) - set(exist_url))

    for eachone in unique_list:
        g_writecount += 1
        output = 'No.' + str(g_writecount) + '\t Depth:' +str(depth) + '\t' + url + ' -> ' + eachone + '\n'
        print(output)
        with open(r'D:\Code\Python\WebScraping\Wikipedia\link_14_3.txt', 'a+') as f:
            f.write(output)
        
        if depth < 2:
            scrappy(eachone, depth+1)

start = time.time()
scrappy('wikipedia')
stop = time.time()
print("深度优先的递归爬虫所用时间：", stop-start)