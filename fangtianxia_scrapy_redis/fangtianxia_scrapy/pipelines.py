# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from fangtianxia_scrapy.items import NewHouseItem, EsfHouseItem
from twisted.enterprise import adbapi
import pymysql
import pymongo

class FangTianXiaScrapyPipeline(object):
    def __init__(self):
        self.newhouse_fp = open('newhouse.json', 'ab')
        self.esfhouse_fp = open('esfhouse.json', 'ab')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fp, ensure_ascii=False)
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fp, ensure_ascii=False)

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.newhouse_exporter.export_item(item)
        elif isinstance(item, EsfHouseItem):
            self.esfhouse_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.newhouse_fp.close()
        self.esfhouse_fp.close()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
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
        dbpool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        if isinstance(item, NewHouseItem):
            insert_sql = """insert into fangtianxia.newhouse(province, city, name, house_type, area, address, 
                            district, sale, price, detail_url)
                            Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(insert_sql, (
                item['province'], item['city'], item['name'], item['house_type'], item['area'], item['address'],
                item['district'], item['sale'], item['price'], item['detail_url']))
        elif isinstance(item, EsfHouseItem):
            insert_sql = """insert into fangtianxia.esfhouse(province, city, name, house_type, area, floor, 
                            orientation, year, address, total_price, unit_price, detail_url)
                            Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(insert_sql, (
                item['province'], item['city'], item['name'], item['house_type'], item['area'], item['floor'],
                item['orientation'], item['year'], item['address'], item['total_price'], item['unit_price'], item['detail_url']))

class MongodbPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[NewHouseItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[EsfHouseItem.collection].create_index([('id', pymongo.ASCENDING)])
        print("打开数据库...")

    def close_spider(self,spider):
        print('写入完毕，关闭数据库.')
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.db[item.collection].update({'detail_url': item['detail_url']}, {'$set': dict(item)}, True)
        elif isinstance(item, EsfHouseItem):
            self.db[item.collection].update({'detail_url': item['detail_url']}, {'$set': dict(item)}, True)
        print('正在写入...')
        return item





