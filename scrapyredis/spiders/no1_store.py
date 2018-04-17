__author__ = 'dailin'

from scrapy import Request
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapyredis.items import SellerInfo
import time


class NumberOneMedicine(RedisCrawlSpider):

    name = 'no1_store'
    allowed_domains = ['111.com.cn','yyh.m.111.com.cn']
    redis_key = 'no1_store:start_urls'
    detailList = ['product']

    custom_settings = {
        'ELASTICSEARCH_SERVERS' : 'http://192.168.2.68',
        'ELASTICSEARCH_PORT' :'9200',
        'ELASTICSEARCH_INDEX' : '111comcn' +  time.strftime("%m%d", time.localtime()) +  'store',
        'ELASTICSEARCH_TYPE' :'store',
        'ELASTICSEARCH_UNIQ_KEY' : 'company_name',
        'ELASTICSEARCH_BUFFER_LENGTH' : 50,
        'ITEM_PIPELINES':{'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 1}
    }

    rules = (
        # 只提取复合规则的页面链接，不做分析，所以跟页面但是没有，follow是对网易深一层的爬取，false表示不提取连接，也不请求页面上的连接
        Rule(LinkExtractor(allow=r'categories/\d*?-j\d*?'), follow=True),
        Rule(LinkExtractor(allow=r'list/.*?'),follow=True),
        Rule(LinkExtractor(allow=r'product/\d+?'), follow=False,callback='parse_store'),
    )

    def parse_store(self,response):
        shop_name = ''  # 店铺名称
        company_name = ''  # 公司名称
        contact_way = ''  # 联系方式
        company_position = ''  # 公司位置
        info_time = ''  # 信息获取时间
        try:
            if '自营' in response.xpath("//div[@class='middle_property']/span[1]/text()").extract()[0].strip():
                return
            else:
                item = SellerInfo()

                url = response.xpath("//div[@class='right_property']/h3/a[1]/@href").extract()[0].strip()

                if len(response.xpath("//div[@class='right_property']/h3/a[1]/text()").extract()) >= 1:
                    shop_name = response.xpath("//div[@class='right_property']/h3/a[1]/text()").extract()[0].strip()

                info_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                if len(response.xpath("//div[@class='right_property']//ul[@class='info_list pl10 pr10']/li[1]/span[2]/text()").extract()) >= 1:
                    company_name = \
                    response.xpath("//div[@class='right_property']//ul[@class='info_list pl10 pr10']/li[1]/span[2]/text()").extract()[0].strip()

                if len(response.xpath("//div[@class='right_property']//ul[@class='info_list pl10 pr10']/li[3]/text()").extract()) >= 1:
                    contact_way = response.xpath("//div[@class='right_property']//ul[@class='info_list pl10 pr10']/li[3]/text()").extract()[0].strip()  # 药品规格

                if len(response.xpath("//div[@class='right_property']//ul[@class='info_list pl10 pr10']/li[2]/text()").extract()) >= 1:
                    company_position = response.xpath("//div[@class='right_property']//ul[@class='info_list pl10 pr10']/li[2]/text()").extract()[0].strip()


                item['shop_name'] = shop_name
                item['info_time'] = info_time
                item['company_name'] = company_name
                item['contact_way'] = contact_way
                item['company_position'] = company_position
                item['store_site'] = url

                yield  item
        except Exception as e:

            print(e)


    # def parse_item(self, response):
    #     shop_name = ''  # 店铺名称
    #     company_name = ''  # 公司名称
    #     contact_way = ''  # 联系方式
    #     company_position = ''  # 公司位置
    #     yyzz = ''  # 营业执照
    #     jyxkz = ''  # 经营许可证
    #     gsp = ''  # GSP证号
    #     jyfw = ''  # 经营范围
    #     info_time = ''  # 信息获取时间
    #
    #     try:
    #         item = SellerInfo()
    #
    #         if len(response.xpath("//div[@class='shop_name']/text()").extract())>=1:
    #             shop_name = response.xpath("//div[@class='shop_name']/text()").extract()[0].strip()
    #
    #         info_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #
    #         if len(response.xpath("//div[@class='company_info']/div[1]/text()").extract())>=1:
    #             company_name = response.xpath("//div[@class='company_info']/div[1]/text()").extract()[0].strip().split(":")[1]
    #
    #         if len(response.xpath("//div[@class='company_info']/div[1]/text()").extract())>=1:
    #             contact_way = response.xpath("//div[@class='company_info']/div[1]/text()").extract()[0].strip()# 药品规格
    #
    #         if len (response.xpath("//div[@class='company_info']/div[2]/text()").extract())>=1:
    #             company_position = response.xpath("//div[@class='company_info']/div[2]/text()").extract()[0].strip()# 药品类型
    #
    #         print("company_name:{0}".format(company_name))
    #         print("shop_name:{0}".format(shop_name))
    #         print("contact_way:{0}".format(contact_way))
    #         print("info_time:{0}".format(info_time))
    #         print("yyzz:{0}".format(yyzz))
    #
    #
    #
    #         item['shop_name'] = shop_name
    #         item['info_time'] = info_time
    #         item['company_name'] = company_name
    #         item['contact_way'] = contact_way
    #         item['company_position'] = company_position
    #         item['yyzz'] = yyzz
    #         item['jyxkz'] = jyxkz
    #         item['gsp'] = gsp
    #         item['jyfw'] = jyfw
    #
    #         yield item
    #
    #     except Exception as e:
    #
    #         print(e)


