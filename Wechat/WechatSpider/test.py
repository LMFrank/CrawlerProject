import requests
from pyquery import PyQuery as pq

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1569158755&ver=1868&signature=*VPDPzbOLwhBCbgkk5qiJMB6eKk5Yvv3Fh2KWuGFm5zGVbL7W4fpSqHum38iK4iFhIBD174OMv9gHOWhxS30eOIvVHCG70RaRFYPB45OoFH01XTW5NILNjVldr7E**K8&new=1'
r = requests.get(url, headers=headers)
doc = pq(r.text)
# title = doc('.rich_media_title').text()
nickname = doc('#js_profile_qrcode p:nth-child(3) span').text()
print(nickname)