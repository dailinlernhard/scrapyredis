__author__ = 'dailin'

from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyredis.items import Yaoq
import uuid
import time


class JDMedicine(RedisCrawlSpider):

    name = 'jd_medicine'
    allowed_domains = ['yao.jd.com']
    redis_key = 'jd_medicine:start_urls'

    custom_settings = {
        'ELASTICSEARCH_SERVERS': 'http://192.168.2.68',
        'ELASTICSEARCH_PORT': '9200',
        'ELASTICSEARCH_INDEX': 'yaojdcom' + time.strftime("%m%d", time.localtime()) + 'medicine',
        'ELASTICSEARCH_TYPE': 'medicine',
        # 'ELASTICSEARCH_UNIQ_KEY' : 'company_name',
        'ELASTICSEARCH_BUFFER_LENGTH': 50,
        'ITEM_PIPELINES': {'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 1}
    }

    rules = (
        Rule(LinkExtractor(allow=r'wareSearch/searchByKeyWord?cat\d+?Id=\d+?'), follow=True),
        Rule(LinkExtractor(allow=r'wareSearch/searchByKeyWord?cat\d+?Id=\d+?&currentPage=\d+?'), follow=True),
        # 只提取复合规则的页面链接，不做分析，所以跟页面但是没有，follow是对网易深一层的爬取，false表示不提取连接，也不请求页面上的连接
        Rule(LinkExtractor(allow=r'item/\d+?.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        try:
            item = Yaoq()
            # print(response.text)
            author = response.xpath("//div[@class='pti']//div[@class='authi']/a[1]/text()").extract()[0]
            authorLocation = response.xpath("//div[@class='pti']//div[@class='authi']/a[1]/@href").extract()[0]
            pubDate = response.xpath("//div[@class='pti']//div[@class='authi']//em[1]/text()").extract()[0]
            # 提取所有文本
            content = \
            response.xpath("//div[@class='pcb']//div[@class='t_fsz']/table[1]//tr")[0].xpath('string(.)').extract()[0]
            contentData = content.replace("\r\n", "")
            title = response.xpath("//span[@id='thread_subject']/text()").extract()[0]

            print(author)
            print(authorLocation)
            print(pubDate)
            print(contentData)
            print(title)

            item['title'] = title
            item['pubDate'] = pubDate
            item['author'] = author
            item['authorLocation'] = authorLocation
            item['content'] = contentData
            item['id'] = str(uuid.uuid1())
            yield item
        except BaseException as e:
            print(e)


