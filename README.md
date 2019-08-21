# CrawlerProject
个人练习的一些爬虫项目
## 链家网爬虫项目
同步爬取：[tongbu.py](https://github.com/LMFrank/CrawlerProject/blob/master/LianJia/tongbu.py)

异步爬取：[yibu.py](https://github.com/LMFrank/CrawlerProject/blob/master/LianJia/yibu.py)

有待改进：

1、可以提前定制好csv输入内容，然后将to_csv移至每一次爬取内，这样可以实现即时保存，防止意外；

2、加入aiomultiprocessing库， 实现异步获得url，并发处理页面详细内容；

3、表结构设计有不合理处，楼层可使用正则表达式直接获取，从而删除包含建造时间的字段。
## Wikipedia项目
* [深度优先的递归爬虫](https://github.com/LMFrank/CrawlerProject/blob/master/Wikipedia/Depth_First.py)
* [广度优先的多线程爬虫](https://github.com/LMFrank/CrawlerProject/blob/master/Wikipedia/Breadth_First.py)
## BaiduAPI项目
通过百度地图api获取全中国有关公园的信息，并且保存至mysql，注意表结构设计应遵循三范式

## 爬取虎扑步行街项目
爬取虎扑步行街的帖子，并存储信息至MongoDB

写了个简单的MongoAPI，用于在爬虫文件中调用pymongo的操作

问题：1、只能爬取前10页，我认为应该是10页后需要登录才可以继续爬取。可以加入cookies解决反爬虫问题。
