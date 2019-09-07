# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    collection = 'newhouse'

    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    house_type = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    sale = scrapy.Field()
    price = scrapy.Field()
    detail_url = scrapy.Field()

class EsfHouseItem(scrapy.Item):
    collection = 'esfhouse'

    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    house_type = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    orientation = scrapy.Field()
    year = scrapy.Field()
    address = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    detail_url = scrapy.Field()
