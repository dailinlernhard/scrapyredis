# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyredisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Yaoq(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    pubDate = scrapy.Field()
    author = scrapy.Field()
    authorLocation = scrapy.Field()
    content = scrapy.Field()

class SellerInfo(scrapy.Item):
    shop_name = scrapy.Field() # 店铺名称
    company_name = scrapy.Field() # 公司名称
    contact_way = scrapy.Field() # 联系方式
    company_position = scrapy.Field() # 公司位置
    yyzz = scrapy.Field() # 营业执照
    jyxkz = scrapy.Field() # 经营许可证
    gsp = scrapy.Field() # GSP证号
    jyfw = scrapy.Field() # 经营范围
    info_time = scrapy.Field() # 信息获取时间
    store_site = scrapy.Field() # 店铺网址
    adcode = scrapy.Field() # 店铺网址
    district = scrapy.Field() # 店铺网址
    city = scrapy.Field() # 店铺网址


class Medicine(scrapy.Item):
    website_name = scrapy.Field() #网站名称
    website_location = scrapy.Field() #网站地址
    website_ip = scrapy.Field() # 网站ip

    store = scrapy.Field() #店铺名称

    information_time = scrapy.Field() # 信息获取时间

    medicine_name = scrapy.Field() # 药品名称
    medicine_type = scrapy.Field() # 药品类别
    specifications = scrapy.Field() # 药品规格
    jx = scrapy.Field() # 剂型
    pzwh = scrapy.Field() # 批准文号
    enterprise = scrapy.Field() # 生产企业
    distributor = scrapy.Field() # 经销商
    brand = scrapy.Field() #  品牌
    price = scrapy.Field() # 价格
    sale_date = scrapy.Field() # 上架时间
    medicine_description = scrapy.Field() # 产品介绍
    instructions = scrapy.Field() # 产品说明书
    month_sales = scrapy.Field() # 月销量
    deliver_place = scrapy.Field() # 发货地
    authentication = scrapy.Field() # 经营认证
    distribution_type = scrapy.Field() # 配送方式
    common_name = scrapy.Field() # 通用名
    keyword = scrapy.Field() # 关键字
    source_type = scrapy.Field() # 来源类型
    batch_number = scrapy.Field() # 批号
    produce_time = scrapy.Field() # 生产时间
    period_validity = scrapy.Field() # 有效期
    screen_shot = scrapy.Field() # 快照



