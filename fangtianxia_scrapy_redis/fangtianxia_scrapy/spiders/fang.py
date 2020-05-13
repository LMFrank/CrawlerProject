# -*- coding: utf-8 -*-
import scrapy
import re
from fangtianxia_scrapy.items import NewHouseItem, EsfHouseItem
from scrapy_redis.spiders import RedisSpider

class FangSpider(RedisSpider):
    name = 'fang'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = 'fang:start_urls'

    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr')
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            province_td = tds[0]
            province_text = province_td.xpath('.//text()').get()
            province_text = re.sub(r'\s', '', province_text)
            if province_text:
                province = province_text
            # 不爬取海外城市的房源
            if province == '其它':
                continue

            city_td = tds[1]
            city_links = city_td.xpath('.//a')
            for city_link in city_links:
                city = city_link.xpath('.//text()').get()
                # 台湾url地址与其他不同
                if '台湾' in city:
                    continue
                # 北京二手房页面会重定向至本地，还未解决该问题
                if '北京' in city:
                    continue
                city_url = city_link.xpath('.//@href').get()
                city_text = re.findall('.*//(.*).*.fang', city_url)[0]
                # 构建新房的url链接
                newhouse_url = 'https://' + city_text + '.newhouse.fang.com/house/s/'
                # 构建二手房的url链接
                esf_url = 'https://' + city_text + '.esf.fang.com'

                # print(f'城市: {province},{city}')
                # print(f'城市链接: {city_url}')
                # print(f'新房链接：{newhouse_url}')
                # print(f'二手房链接: {esf_url}')
                # print(f'租房链接: {zf_url}')

                yield scrapy.Request(
                    url=newhouse_url,
                    callback=self.parse_newhouse,
                    meta={'info': (province, city)}
                )
                yield scrapy.Request(
                    url=esf_url,
                    callback=self.parse_esf,
                    meta={'info': (province, city)}
                )
            #     break
            # break

    def parse_newhouse(self, response):
        # 新房
        province, city = response.meta.get('info')
        lis = response.xpath('//div[contains(@class,"nl_con clearfix")]/ul/li')
        for li in lis:
            # 页面中插入了广告页li，需要剔除
            name_text = li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            name = name_text.strip()
            if name:
                house_type_list = li.xpath('.//div[contains(@class, "house_type")]/a/text()').getall()
                house_type_list = list(map(lambda x: re.sub(r'/s', '', x), house_type_list))
                house_type = ','.join(list(filter(lambda x: x.endswith('居'), house_type_list)))
                # house_type = '/'.join(house_type_list)
                area_text = ''.join(li.xpath('.//div[contains(@class, "house_type")]/text()').getall())
                area = re.sub(r'\s|－|/', '', area_text)
                address = li.xpath('.//div[@class="address"]/a/@title').get()
                district_text = ''.join(li.xpath('.//div[@class="address"]/a//text()').getall())
                try:
                    district = re.search(r'.*\[(.+)\].*', district_text).group(1)
                except:
                    district = 'None'
                sale = li.xpath('.//div[contains(@class, "fangyuan")]/span/text()').get()
                price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
                price = re.sub(r"\s|广告", "", price)
                # price1 = li.xpath('.//div[@class="nhouse_price"]/span/text()').get()
                # price2 = li.xpath('.//div[@class="nhouse_price"]/em/text()').get()
                # try:
                #     price = price1 + price2
                # except:
                #     price = None
                detail_url_text = li.xpath('.//div[@class="nlc_img"]/a/@href').get()
                detail_url = response.urljoin(detail_url_text)
                item = NewHouseItem(province=province, city=city, name=name, house_type=house_type, area=area,
                                    address=address, district=district, sale=sale, price=price, detail_url=detail_url)
                yield item

        next_url = response.xpath('//div[@class="page"]//a[class="next"]/@href').get()
        print(next_url)
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),
                                 callback=self.parse_newhouse,
                                 meta={'info': (province, city)})


    def parse_esf(self, response):
        # 二手房
        province, city = response.meta.get('info')
        dls = response.xpath('//div[@class="shop_list shop_list_4"]/dl')
        for dl in dls:
            item = EsfHouseItem(province=province, city=city)
            name = dl.xpath('.//span[@class="tit_shop"]/text()').get()
            # 页面中插入了广告页li，需要剔除
            if name:
                infos = dl.xpath('.//p[@class="tel_shop"]/text()').getall()
                infos = list(map(lambda x: re.sub(r"\s", "", x), infos))
                for info in infos:
                    if "厅" in info:
                        item["house_type"] = info
                    elif '㎡' in info:
                        item["area"] = info
                    elif '层' in info:
                        item["floor"] = info
                    elif '向' in info:
                        item["orientation"] = info
                    elif '年建' in info:
                        item["year"] = re.sub("年建", "", info)
                item["address"] = dl.xpath('.//p[@class="add_shop"]/span/text()').get()
                item["total_price"] = "".join(dl.xpath(".//span[@class='red']//text()").getall())
                item["unit_price"] = dl.xpath(".//dd[@class='price_right']/span[2]/text()").get()
                item["detail_url"] = response.urljoin(dl.xpath(".//h4[@class='clearfix']/a/@href").get())
                item["name"] = name
                # 以下五个字段大概率会缺失，存入mysql会报错，因此加入判断
                if 'house_type' not in item:
                    item["house_type"] = '/'
                elif 'area' not in item:
                    item["area"] = '/'
                elif 'floor' not in item:
                    item["floor"] = '/'
                elif 'orientation' not in item:
                    item["orientation"] = '/'
                elif 'year' not in item:
                    item["year"] = '/'
                yield item
            next_url = response.xpath('//div[@class="page_al"]/p/a/@href').get()
            if next_url:
                yield scrapy.Request(url=response.urljoin(next_url),
                                     callback=self.parse_esf,
                                     meta={'info': (province, city)})