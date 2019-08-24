# CrawlerProject
个人练习的一些爬虫项目
## 链家网二手房源爬虫项目
链家网的显示方式为每页30条房源数据，最多显示100页，即3000条。因此，我使用二分法切割价格区间，从而得到完整数据。

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

## 链家网租房爬虫项目（Scrapy+异步MySQL）
刚好需要租房，因此写了这个爬虫项目。

同步写入数据速度比较慢，而爬虫速度比较快，可能出现数据最后写入不到数据库中的情况，因此可以使用异步框架twisted解决这个问题。

在pipeline.py中我重写了异步MySQL方法，同时settings中需要设置数据库连接参数，并且更改ITEM_PIPELINES的参数。

![数据库连接参数](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/settings.jpg) ![ITEM_PIPELINES的参数](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/item_pipeline.jpg)

链家网的显示方式为每页30条房源数据，最多显示100页，即3000条。因此，可以使用之前提到的使用二分法切割价格区间，从而得到完整数据。

食用方法：
1. 运行creat_table.py建表
2. 对于大于3000条房源信息的获取需求，目前方案是先通过[get_url_list.py](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/get_url_list.py)去获取需要的价格范围，并将得到的url存储至txt文件中，然后在lianjiazufang.py中获取url并添加至start_urls，运行爬虫

~~等待填坑：毫无疑问，使用scrapy+redis能够更好地动态添加、获取信息~~

在爬取过程中我发现链家网的租房方式除了普通房源以外，还有一种是公寓。爬虫里写的url地址是普通房源形式，而公寓房源的详情页是以另外一种结构的url，且显示的页面也不同，如有需求，可加上对公寓的判断。

![普通房源](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/%E6%99%AE%E9%80%9A.png) ![公寓房源](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/%E5%85%AC%E5%AF%93.jpg)

![MySQL效果图](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/mysql.jpg)




