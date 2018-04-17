__author__ = 'dailin'

from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapyredis.items import Medicine
import time


class NumberOneMedicine(RedisCrawlSpider):

    name = 'no1_medicine'
    allowed_domains = ['111.com.cn']
    redis_key = 'no1:start_urls'
    detailList = ['product'] # 启用selenium页面链接列表

    custom_settings = {
        'ELASTICSEARCH_SERVERS' : 'http://192.168.2.68',
        'ELASTICSEARCH_PORT' :'9200',
        'ELASTICSEARCH_INDEX' : '111comcn' +  time.strftime("%m%d", time.localtime()) +  'medicine',
        'ELASTICSEARCH_TYPE' :'medicine',
        # 'ELASTICSEARCH_UNIQ_KEY' : 'company_name',
        'ELASTICSEARCH_BUFFER_LENGTH' : 50,
        'ITEM_PIPELINES':{'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 1}
    }

    rules = (
        # 只提取复合规则的页面链接，不做分析，所以跟页面但是没有，follow是对网易深一层的爬取，false表示不提取连接，也不请求页面上的连接
        Rule(LinkExtractor(allow=r'categories/\d*?-j\d*?.html'), follow=True),
        Rule(LinkExtractor(allow=r'list/.*?.html'),follow=True),
        Rule(LinkExtractor(allow=r'product/\d+?.html'), follow=False, callback='parse_item')
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
        store = '1药网'
        common_name = ''
        distribution_type = ''
        period_validity = ''
        try:
            item = Medicine()

            if len(response.xpath("//div[@class='middle_property']/span[1]/text()").extract())>=1:
                if '自营' in response.xpath("//div[@class='middle_property']/span[1]/text()").extract()[0].strip():
                    store = '1药网'
                else:
                    if len(response.xpath("//div[@class='right_property']//a[1]/text()").extract())>=1:
                        store = response.xpath("//div[@class='right_property']//a[1]/text()").extract()[0].strip() # 店铺

            information_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 信息获取时间

            if len(response.xpath("//div[@class='goods_intro']//tr[1]//td/text()").extract())>=1:
                medicine_name = response.xpath("//div[@class='goods_intro']//tr[1]//td/text()").extract()[0].strip() # 药品名

            if len(response.xpath("//div[@class='goods_intro']//tr[2]//td[2]/text()").extract())>=1:
                specifications = response.xpath("//div[@class='goods_intro']//tr[2]//td[2]/text()").extract()[0].strip()# 药品规格

            if len (response.xpath("//div[@class='goods_intro']//tr[4]//td[2]/text()").extract())>=1:
                medicine_type = response.xpath("//div[@class='goods_intro']//tr[4]//td[2]/text()").extract()[0].strip()# 药品类型

            # jx = response.xpath("//div[@class='pcb']//div[@class='t_fsz']/table[1]//tr")[0].xpath('string(.)').extract()[0] # 剂型
            pzwh = response.xpath("//div[@class='goods_intro']//tr[4]//td[1]")[0].xpath('string(.)').extract()[0].strip() # 批准文号
            # contentData = content.replace("\r\n", "")
            enterprise = response.xpath("//div[@class='goods_intro']//tr[3]//td[2]/text()").extract()[0].strip() # 生产企业
            # distributor = response.xpath("//div[@class='goods_intro']//tr[3]//td[2]/text()").extract()[0] # 经销商
            brand = response.xpath("//div[@class='goods_intro']//tr[2]//td[1]/text()").extract()[0].strip() # 品牌

            if len(response.xpath("//span[@class='good_price']/text()").extract()) >= 1:
                price = response.xpath("//span[@class='good_price']/text()").extract()[0].strip().replace("￥",'') # 价格
            if len(response.xpath("//span[@class='good_price good_price01']/text()")) >= 1:
                price = response.xpath("//span[@class='good_price good_price01']/text()").extract()[0].strip().replace("￥", '')  # 价格
            # sale_date = response.xpath("//span[@class='good_price']/text()").extract()[0] # 上架时间

            instructions = ''
            info_table = response.xpath("//table[@class='specificationBox']")

            if len(info_table)>=1 :
                instructions = info_table[0].xpath('string(.)').extract()[0]

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
            if len(response.xpath("//dl[@class='clearfix btnCartDl']//dd[2]//p/text()")) >= 1:
                distribution_type = response.xpath("//dl[@class='clearfix btnCartDl']//dd[2]//p/text()").extract()[0].strip() # 配送方式


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

            item['store'] = store
            item['information_time'] = information_time
            item['medicine_name'] = medicine_name
            item['specifications'] = specifications
            item['medicine_type'] = medicine_type
            item['pzwh'] = pzwh
            item['enterprise'] = enterprise
            item['brand'] = brand
            item['price'] = price
            item['instructions'] = instructions
            item['distribution_type'] = distribution_type
            item['period_validity'] = period_validity
            item['common_name'] = common_name

            yield item

        except Exception as e:
            print("=========出现异常")
            print("store:{0}".format(store))
            print("information_time:{0}".format(information_time))
            print("medicine_name:{0}".format(medicine_name))
            print("specifications:{0}".format(specifications))
            print("medicine_type:{0}".format(medicine_type))
            print("pzwh:{0}".format(pzwh))
            print("enterprise:{0}".format(enterprise))
            print("brand:{0}".format(brand))
            print("price:{0}".format(price))
            print("instructions:{0}".format(instructions))
            print("distribution_type:{0}".format(distribution_type))
            print("period_validity:{0}".format(period_validity))
            print("common_name:{0}".format(common_name))
            print(e)


