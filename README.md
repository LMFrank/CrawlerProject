# CrawlerProject

- [1.1 链家网二手房源](https://github.com/LMFrank/CrawlerProject/tree/master/LianJia)
- [1.2 Wikipedia](https://github.com/LMFrank/CrawlerProject/tree/master/Wikipedia)
- [1.3 BaiduAPI](https://github.com/LMFrank/CrawlerProject/tree/master/baidumapapi)
- [1.4 爬取虎扑步行街](https://github.com/LMFrank/CrawlerProject/tree/master/Hupu)
- [1.5 链家网租房爬虫项目（Scrapy+异步MySQL）](https://github.com/LMFrank/CrawlerProject/tree/master/lianjia_scrapy)
- [1.6 房天下新房、二手房爬虫项目（Scrapy-Redis分布式爬虫)](https://github.com/LMFrank/CrawlerProject/tree/master/fangtianxia_scrapy_redis)
- [1.7 微信公众号（通过代理池爬取）](https://github.com/LMFrank/CrawlerProject/tree/master/Wechat)

**NOTE:**

1. 开发环境：Win10(WSL-Ubuntu、VBox-Ubuntu) + Anaconda3 + PyCharm(VSCode) + Cmder + XShell

2. WSL环境的搭建可参考我写的博文：[打造Win10+WSL开发环境【图文】](https://blog.csdn.net/LMFranK/article/details/100214551)

3. VSCode Insider版本实现win10下远程连接WSL编写代码更加方便

4. WSL的文件共享推荐XShell，VBox直接使用共享文件夹。如果使用Pycharm，可以直接进入tools-Deployment-configuration，创建sftp连接

5. 终端强烈推荐Cmder，可以直接进入WSL环境

6. 所有项目的包依赖集合在[requirements.txt](https://github.com/LMFrank/CrawlerProject/blob/master/requirements.txt)，其中因为部署在linux服务器上，所以我删除了pywin32包及mkl包，有需求可以自行添加

***


### 1.1 链家网二手房源
链家网的显示方式为每页30条房源数据，最多显示100页，即3000条。因此，我使用二分法切割价格区间，从而得到完整数据。

同步爬取：[tongbu.py](https://github.com/LMFrank/CrawlerProject/blob/master/LianJia/tongbu.py)（requests+xpath)

异步爬取：[yibu.py](https://github.com/LMFrank/CrawlerProject/blob/master/LianJia/yibu.py)（asyncio+aiohttp+xpath)

有待改进：

1、可以提前定制好csv输入内容，然后将to_csv移至每一次爬取内，这样可以实现即时保存，防止意外；

2、加入aiomultiprocessing库， 实现异步获得url，并发处理页面详细内容；

3、表结构设计有不合理处，楼层可使用正则表达式直接获取，从而删除包含建造时间的字段。

***

### 1.2 Wikipedia
* [深度优先的递归爬虫](https://github.com/LMFrank/CrawlerProject/blob/master/Wikipedia/Depth_First.py)
* [广度优先的多线程爬虫](https://github.com/LMFrank/CrawlerProject/blob/master/Wikipedia/Breadth_First.py)

***

### 1.3 BaiduAPI
通过百度地图api获取全中国有关公园的信息，并且保存至mysql，注意表结构设计应遵循三范式

***

### 1.4 爬取虎扑步行街
爬取虎扑步行街的帖子，并存储信息至MongoDB

写了个简单的MongoAPI，用于在爬虫文件中调用pymongo的操作

问题：1、只能爬取前10页，应该是10页后需要登录才可以继续爬取。可以加入cookies解决反爬虫问题。

***

### 1.5 链家网租房爬虫项目（Scrapy+异步MySQL）
刚好需要租房，因此写了这个爬虫项目。目前网络上分享的关于链家网租房的爬虫项目似乎都已落后于网页更新，应该是今年链家网对租房页面进行了参数的重构。我提供的代码适配最新的租房网页，请放心食用:yum:，如果出现变动请告知。

同步写入数据速度比较慢，而爬虫速度比较快，可能出现数据最后写入不到数据库中的情况，因此可以使用异步框架twisted解决这个问题。

在pipeline.py中我重写了异步MySQL方法，同时settings中需要设置数据库连接参数，并且更改ITEM_PIPELINES的参数。

![数据库连接参数](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/settings.jpg) ![ITEM_PIPELINES的参数](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/item_pipeline.jpg)

链家网的显示方式为每页30条房源数据，最多显示100页，即3000条。因此，可以使用之前提到的使用二分法切割价格区间，从而得到完整数据。

食用方法：
1. 运行creat_table.py建表
2. 对于大于3000条房源信息的获取需求，目前方案是先通过[get_url_list.py](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/get_url_list.py)去获取需要的价格范围，并将得到的url存储至txt文件中，然后在lianjiazufang.py中获取url并添加至start_urls，运行爬虫

等待填坑：
1. 毫无疑问，使用scrapy+redis能够更好地动态添加、获取信息
2. 结合高德地图api将爬取数据可视化。由于创建可视化地图需要房源的对应的经纬度，~~而在房源详情页中，我发现链家网使用了百度地图api的jsapi服务，生成了动态地图，可能导致无法获得具体经纬度。因此目前先使用笨办法，将已爬取的数据结合百度api项目，爬取对应的经纬度数据~~仔细查看后，发现经纬度数据在<script>标签里，因此直接通过正则表达式获取

在爬取过程中我发现链家网的租房方式除了普通房源以外，还有一种是公寓。爬虫里写的url地址是普通房源形式，而公寓房源的详情页是另外一类url，且显示的页面也不同，如有需求，可加上对公寓的判断。

![普通房源](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/%E6%99%AE%E9%80%9A.png) ![公寓房源](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/%E5%85%AC%E5%AF%93.jpg)

![MySQL效果图](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/mysql.jpg)

数据可视化填坑完毕![效果图](https://github.com/LMFrank/CrawlerProject/blob/master/lianjia_scrapy/imgs/%E9%AB%98%E5%BE%B7api.jpg)
在该项目中我爬取了链家网南京租房房源，单价在0-3000元/月，一共获得了34086条数据，略少于链家网显示的36997条。主要原因是之前提到的公寓获取问题，以及scrapy爬取过程中的自动去重。

~~吐槽：NJU仙林校区周围的房源非常少，但是都很贵，目测房源都在坑爹的二房东手里~~

联系了高德地图平台的客服，表示高德地图可视化api的分享功能最近在维护，因此网页源代码还无法提供。

***

### 1.6 房天下新房、二手房爬虫项目（Scrapy-Redis分布式爬虫)
该项目基于Scrapy-Redis框架实现分布式爬虫。其中，我使用了自身电脑（win10）作为master, WSL虚拟机和一台mac作为slave，从而实现分布式爬虫。

关于房天下的爬虫网络上有很多，但是实际运行后，会有一些问题。比如，目前房天下的城市房源页面加入了广告页，这是爬取过程中不需要的数据，如果不处理，会直接报错，停止爬虫运行。在该项目中我对遇到的问题进行了优化，具体已经在代码里进行了注释。

**更新：**



2019/09/07

1. 加入了MongodbPipeline：在实际爬取过程中，经常出现数据存入mysql发生错误，这是由于爬取过程中，字段缺失导致入库时不匹配造成的。因此，加入了mongodb这种非关系型数据库，帮助存储数据

2. 改变了存储模式，之前打开了RedisItem，但是把redis作为数据存储比较浪费，因此将请求队列和数据存储区分开来，远程连接mongodb完成数据入库的工作

   

**改造成分布式爬虫：**

1. 首先安装scrapy-redis
2. 将爬虫的类从 scrapy.Spider 变成 scrapy_redis.spiders.RedisSpider
3. 将爬虫中的start_urls删掉。增加一个redis_key="xxx"。这个redis_key是为了以后在redis中控制爬虫启动的。爬虫的第一个url，就是在redis中通过这个发送出去的
![fang](https://github.com/LMFrank/CrawlerProject/blob/master/fangtianxia_scrapy_redis/imgs/fang.jpg)
4. 更改scrapy的配置文件，将爬虫的去重交由redis完成，并将结果存储至redis
![settings](https://github.com/LMFrank/CrawlerProject/blob/master/fangtianxia_scrapy_redis/imgs/settings.jpg)
如果redis服务器需求密码，应添加REDIS_PASSWORD='your password'项，这里提供另外一种方式，一行命令即可，即REDIS_URL:
>REDIS_URL='redis://:password@ip:port'

**运行爬虫：**
1. 在爬虫服务器上，进入爬虫文件所在的路径，然后输入命令：
>scrapy runspider 爬虫名

不再是scrapy crawl 爬虫名



2. 在Redis服务器上，推入一个开始的url链接：
>redis-cli> lpush [redis_key] start_url

开始爬取

**NOTE:**

1. 如果设置了LOG_FILE，那么爬虫报错时，终端只会出现：
>Unhandled error in Deferred

![error](https://github.com/LMFrank/CrawlerProject/blob/master/fangtianxia_scrapy_redis/imgs/linux_error.jpg)
   此时，应进入.log文档内查看错误

2. 查看防火墙是否阻挡连接，redis设置远程连接时，应注释掉redis.conf里的"bind 127.0.0.1"字段

**以上爬虫项目均用于学习，不用于任何商业目的。**

***

### 1.7 微信公众号（通过代理池爬取）
微信公众号的爬取是基于[搜狗微信](https://weixin.sogou.com/)，未登录只能获取10页，登录后即可获取最多100页的内容。在前期测试过程中发现，搜狗微信封ip非常快，因此使用已搭建好的[代理池](https://github.com/LMFrank/ProxyPool)进行爬取。

**NOTE:**

1. 代理池需要更改settings.py中的TEST_URL参数，将其修改为你需要测试的url
2. 实际测试发现，如果使用免费代理，即使使用了代理池中评分最高，也基本都会被封。因此，因此如果有需求，需要自行添加高质量代理
3. 该项目基本思路基于《Python3网络爬虫开发实战》


