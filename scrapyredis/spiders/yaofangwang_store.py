__author__ = 'dailin'

from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapyredis.items import SellerInfo
from scrapy import Request
import time
from scrapyredis.tool.position_util import PositionUtil


class YaoFangWang(RedisCrawlSpider):

    name = 'yaofangwang_store'
    allowed_domains = ['www.yaofangwang.com']
    redis_key = 'yaofangwang_store:start_urls'
    detailList = []

    custom_settings = {
        'ELASTICSEARCH_SERVERS' : 'http://192.168.2.68',
        'ELASTICSEARCH_PORT' :'9200',
        'ELASTICSEARCH_INDEX' : 'yaofangwangcom' +  time.strftime("%m%d", time.localtime()) +  'store',
        'ELASTICSEARCH_TYPE' :'store',
        'ELASTICSEARCH_UNIQ_KEY' : 'company_name',
        'ELASTICSEARCH_BUFFER_LENGTH' : 3,
        'ITEM_PIPELINES':{'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 1}
    }

    rules = (
        Rule(LinkExtractor(allow=r'yaofangwang.com/Catalog-\d*?.html$'), follow=True),
        Rule(LinkExtractor(allow=r'yaofangwang.com/catalog-\d*?-p\d*?.html$'),follow=True),
        Rule(LinkExtractor(allow=r'yaofangwang.com/medicine-\d*?.html$'), follow=True,callback='parse_store'),
        Rule(LinkExtractor(allow=r'medicine-\d+?-p\d*?'), follow=True,callback='parse_store'),
        # Rule(LinkExtractor(allow=r'yaodian'), follow=True, callback='parse_item')
    )

    def parse_store(self,response):
        shopList = response.xpath("//div[@class='shop']")

        for shop in  shopList:
            shopUrl = shop.xpath(".//p[@class='clearfix']//a/@href").extract()[0].strip()
            self.log("++++++++++获取到店铺：https:" + shopUrl)
            yield Request(url="https:" + shopUrl,callback=self.parse_item)



    def parse_item(self, response):
        company_name = ''  # 公司名称
        # contact_way = ''  # 联系方式
        company_position = ''  # 公司位置
        info_time = ''  # 信息获取时间
        yyzz = ''  # 营业执照
        gsp = '' # GSP证号
        jyxkz = '' # 经营许可证
        jyfw = '' # 经营范围
        adcode = '' # 行政编码
        district = '' # 区
        city = '' # 城市

        try:
            item = SellerInfo()

            if len(response.xpath("//p[@id='morebtn']/text()").extract())>=1:
                company_name = response.xpath("//p[@id='morebtn']/text()").extract()[0].strip() # 店铺名称

                info_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 信息获取时间

            if len(response.xpath("//div[@id='maininfo']//p[2]/text()").extract())>=1:
                company_position = response.xpath("//div[@id='maininfo']//p[2]/text()").extract()[0].strip().split("：")[1] # 店铺地址

            if len(response.xpath("//div[@id='subinfo']//p[1]/text()").extract())>=1:
                yyzz = response.xpath("//div[@id='subinfo']//p[1]/text()").extract()[0].strip().split("：")[1]# 营业执照

            if len(response.xpath("//div[@id='subinfo']//p[2]/text()"))>=1:
                gsp = response.xpath("//div[@id='subinfo']//p[2]/text()").extract()[0].strip().split("：")[1] # GSP证号

            if len(response.xpath("//div[@id='subinfo']//p[3]/text()")) >= 1:
                jyxkz = response.xpath("//div[@id='subinfo']//p[3]/text()").extract()[0].strip().split("：")[1] # 经营许可证

            if len(response.xpath("//div[@id='subinfo']//p[4]/text()")) >= 1:
                jyfw = response.xpath("//div[@id='subinfo']//p[4]/text()").extract()[0].strip().split("：")[1] # 生产企业

            # 地址过滤
            lat,lng = PositionUtil.get_position(company_position)
            province = PositionUtil.get_detail_position(lat,lng)['province']
            self.log("+++++++++++++获取到：{0}的店铺信息".format(province))

            if (province == '吉林省'):
                    item['info_time'] = info_time
                    item['company_name'] = company_name
                    item['yyzz'] = yyzz
                    item['company_position'] = company_position
                    item['store_site'] = response.url
                    item['gsp'] = gsp
                    item['jyxkz'] = jyxkz
                    item['jyfw'] = jyfw
                    item['adcode'] = PositionUtil.get_detail_position(lat,lng)['adcode']
                    item['district'] = PositionUtil.get_detail_position(lat,lng)['district']
                    item['city'] = PositionUtil.get_detail_position(lat,lng)['city']
                    self.log("店铺地址：{0}，省份：{1}".format(company_position,province))

                    yield item

        except Exception as e:
            print("=========出现异常")
            print(e)


