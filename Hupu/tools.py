import requests
from bs4 import BeautifulSoup
import datetime

# 获取页面
def get_page(link):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    r = requests.get(link, headers=headers)
    html = r.content
    html = html.decode('UTF-8')
    soup = BeautifulSoup(html, 'lxml')
    return soup

# 解析网页
def get_data(post_list):
    data_list = []
    for post in post_list:
        title = post.find('div', class_='titlelink box').text.strip()
        post_link = post.find('div', class_='titlelink box').a['href']
        post_link = 'https://bbs.hupu.com' + post_link
        author = post.find('div', class_='author box').a.text.strip()
        author_page = post.find('div', class_='author box').a['href']
        start_date = post.find('div', class_='author box').contents[5].text.strip()
        reply_view = post.find('span', class_='ansour box').text.strip()
        reply = reply_view.split('/')[0].strip()
        view = reply_view.split('/')[1].strip()
        reply_time = post.find('div', class_='endreply box').a.text.strip()
        last_reply = post.find('div', class_='endreply box').span.text.strip()
        if ':' in reply_time:
            date_time = str(datetime.date.today()) + ' ' + reply_time
            date_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M')
        elif reply_time.find('-') == 4:
            date_time = datetime.datetime.strptime(reply_time, '%Y-%m-%d').date()
        else:
            date_time = datetime.datetime.strptime('2019-' + reply_time, '%Y-%m-%d').date()
        data_list.append([title, post_link, author, author_page, start_date, reply, view, last_reply, date_time])
    return data_list

if __name__ == '__main__':
    link = 'https://bbs.hupu.com/bxj'
    soup = get_page(link)
    post_all = soup.find('ul', class_='for-list')
    post_list = post_all.find_all('li')
    data_list = get_data(post_list)
    for each in data_list:
        print(each)
    
