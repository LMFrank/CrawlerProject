# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LianjiaspiderItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    location = scrapy.Field()
    rent = scrapy.Field()
    apartment_layout = scrapy.Field()
    area = scrapy.Field()
    orientation = scrapy.Field()
    publish_time = scrapy.Field()
    unit_price = scrapy.Field()
    floor = scrapy.Field()



