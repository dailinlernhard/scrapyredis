__author__ = 'dailin'

from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapyredis.items import Medicine
import time


class YaoFangWang(RedisCrawlSpider):

    name = 'yaofangwang'
    allowed_domains = ['www.yaofangwang.com']
    redis_key = 'yaofangwang:start_urls'
    detailList = ['detail']

    rules = (
        Rule(LinkExtractor(allow=r'yaofangwang.com/Catalog-\d*?.html'), follow=True),
        Rule(LinkExtractor(allow=r'yaofangwang.com/catalog-\d*?-p\d*?.html'),follow=True),
        Rule(LinkExtractor(allow=r'yaofangwang.com/medicine-\d*?.html'), follow=True),
        Rule(LinkExtractor(allow=r'medicine-\d+?-p\d*?.html'), follow=True),
        Rule(LinkExtractor(allow=r'yaofangwang.com/detail-\d+?.html'), follow=False, callback='parse_item')
    )

    def parse_item(self, response):
        medicine_type = ''
        information_time = ''
        medicine_name = ''
        specifications = ''
        pzwh = ''
        enterprise = ''
        brand = ''
        price = ''
        store = ''
        common_name = ''
        distribution_type = ''
        period_validity = ''
        jx = ''
        screenshot = response.meta['screenshot']
        try:
            item = Medicine()

            if len(response.xpath("//p[@id='morebtn']/text()").extract())>=1:
                store = response.xpath("//p[@id='morebtn']/text()").extract()[0].strip()

            information_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 信息获取时间

            if len(response.xpath("//div//h1//strong/text()").extract())>=1:
                medicine_name = response.xpath("//div//h1//strong/text()").extract()[0].strip() # 药品名

            if len(response.xpath("//dl[@class='summary clearfix']//dd[5]/text()").extract())>=1:
                specifications = response.xpath("//dl[@class='summary clearfix']//dd[5]/text()").extract()[0].strip()# 药品规格

            # if len (response.xpath("//div[@class='goods_intro']//tr[4]//td[2]/text()").extract())>=1:
            #     medicine_type = response.xpath("//div[@class='goods_intro']//tr[4]//td[2]/text()").extract()[0].strip()# 药品类型
            if len(response.xpath("//div[@class='info clearfix']//dd[4]/text()"))>=1:
                jx = response.xpath("//div[@class='info clearfix']//dd[4]/text()").extract()[0].strip() # 剂型
            if len(response.xpath("//dl[@class='summary clearfix']//dd[8]//img/@src")) >= 1:
                pzwh = response.xpath("//dl[@class='summary clearfix']//dd[8]//img/@src").extract()[0].strip() # 批准文号
            # contentData = content.replace("\r\n", "")
            if len(response.xpath("//dl[@class='summary clearfix']//dd[7]/text()")) >= 1:
                enterprise = response.xpath("//dl[@class='summary clearfix']//dd[7]/text()").extract()[0].strip() # 生产企业
            # distributor = response.xpath("//div[@class='goods_intro']//tr[3]//td[2]/text()").extract()[0] # 经销商
            if len(response.xpath("//dl[@class='summary clearfix']//dd[3]/text()")) >= 1:
                brand = response.xpath("//dl[@class='summary clearfix']//dd[3]/text()").extract()[0].strip() # 品牌

            if len(response.xpath("//div[@class='prices clearfix']//span[@class='num v-mid']/text()").extract()) >= 1:
                price = response.xpath("//div[@class='prices clearfix']//span[@class='num v-mid']/text()").extract()[0].strip() # 价格
            else:
                if len(response.xpath("//label[@class='num']/text()").extract()) >= 1:
                    price = response.xpath("//label[@class='num']/text()").extract()[0].strip() # 价格
            # sale_date = response.xpath("//span[@class='good_price']/text()").extract()[0] # 上架时间

            instructions = ''
            info_table = response.xpath("//table[@class='table1 clearfix']")

            if len(info_table)>=1 :
                instructions = "".join(info_table[0].xpath('string(.)').extract()[0].strip().split())
            if len(response.xpath("//dl[@class='summary clearfix']//dd[1]//strong/text()").extract()) >= 1:
                common_name = response.xpath("//dl[@class='summary clearfix']//dd[1]//strong/text()").extract()[0].strip() # 通用名
            # for tr in info_list:
            #     th = tr.xpath('.//th/text()').extract()
            #     td = tr.xpath('.//td/text()').extract()
            #     if len(th)>1:
            #         common_name = '通用名' in th[0].strip() and len(td)>1 if td[0].strip() else '' # 通用
            #
            #         medicine_description += '成分' or '适应症' or '性状' or '规格' in th[0].strip() \
            #                                                          and len(td) > 1 if td[0].strip() else '' # 商品描述
            #
            #         instructions += '用法用量' or '不良反应' or '禁忌' or '注意事项' in th[0].strip() \
            #                       and len(td) > 1 if td[0].strip() else '' # 产品说明书
            #
            #         period_validity = '有效期' in th[0].strip() \
            #                                                 and len(td) > 1 if td[0].strip() else ''  # 有效期

            # 产品说明书
            # if len(response.xpath("//dl[@class='clearfix btnCartDl']//dd[2]//p/text()")) >= 1:
            #     distribution_type = response.xpath("//dl[@class='clearfix btnCartDl']//dd[2]//p/text()").extract()[0].strip() # 配送方式


            # month_sales = response.xpath("//span[@class='good_price']/text()").extract()[0] # 月销量
            # deliver_place = response.xpath("//span[@class='good_price']/text()").extract()[0] # 发货地
            # authentication = response.xpath("//span[@class='good_price']/text()").extract()[0] # 经营认证
            #
            # keyword = response.xpath("//span[@class='good_price']/text()").extract()[0] # 关键字
            # source_type = response.xpath("//span[@class='good_price']/text()").extract()[0] # 来源类型
            # batch_number = response.xpath("//span[@class='good_price']/text()").extract()[0] # 批号
            # produce_time = response.xpath("//span[@class='good_price']/text()").extract()[0] # 生产日期

            # print("store:{0}".format(store))
            # print("information_time:{0}".format(information_time))
            # print("medicine_name:{0}".format(medicine_name))
            # print("specifications:{0}".format(specifications))
            # print("medicine_type:{0}".format(medicine_type))
            # print("pzwh:{0}".format(pzwh))
            # print("enterprise:{0}".format(enterprise))
            # print("brand:{0}".format(brand))
            # print("price:{0}".format(price))
            # print("instructions:{0}".format(instructions))
            # print("distribution_type:{0}".format(distribution_type))
            # print("period_validity:{0}".format(period_validity))
            # print("common_name:{0}".format(common_name))
            # print("jx:{0}".format(jx))

            item['store'] = store
            item['information_time'] = information_time
            item['medicine_name'] = medicine_name
            item['specifications'] = specifications
            item['medicine_type'] = medicine_type
            item['pzwh'] = pzwh
            item['enterprise'] = enterprise
            item['brand'] = brand
            item['jx'] = jx
            item['price'] = price
            item['instructions'] = instructions
            item['distribution_type'] = distribution_type
            item['period_validity'] = period_validity
            item['common_name'] = common_name
            # item['screenshot'] = screenshot # 快照

            yield item

        except Exception as e:
            print("=========出现异常")
            print(e)


