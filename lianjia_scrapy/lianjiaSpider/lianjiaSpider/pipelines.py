# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# Twisted  做异步任务处理的包
# adbapi 操作数据库的模块
from twisted.enterprise import adbapi
import pymysql

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # from_settings 激活pipeline之后，会自动调用该函数加载settings中的配置
    @classmethod
    def from_settings(cls, settings):
        # 准备数据库的链接参数，字典形式
        db_params = dict(
            host=settings['MYSQL_HOST'],
            database=settings['MYSQL_database'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            charset='utf8mb4',
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建连接池
        dbpool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(dbpool)
    
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)  # 异步写入，把执行sql的操作放入pool中
        query.addErrback(self.handle_error, item, spider)  # 执行sql出现错误,会执行指定的回调函数
        return item

    # failure 错误原因
    def handle_error(self, failure, item, spider):
        print(failure)
    
    def do_insert(self, cursor, item):
        insert_sql = """insert into lianjia.spider(title, link, location, rent, apartment_layout, area, oriention, publish_time, unit_price, floor)
                        Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(insert_sql, (item['title'], item['link'], item['location'], item['rent'], item['apartment_layout'], 
                                    item['area'], item['orientation'], item['publish_time'], item['unit_price'], item['floor']))
