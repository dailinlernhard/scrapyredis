__author__ = 'dailin'

from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyredis.items import Yaoq
import uuid
import json


class YaoQ(RedisCrawlSpider):

    name = 'yaoq'
    allowed_domains = ['yaoq.net']

    rules = (
        # 只提取复合规则的页面链接，不做分析，所以跟页面但是没有，follow是对网易深一层的爬取，false表示不提取连接，也不请求页面上的连接
        Rule(LinkExtractor(allow=r'www.yaoq.net/thread.*\.html'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'www.yaoq.net/forum-95-\d+\.html'), follow=True)
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


