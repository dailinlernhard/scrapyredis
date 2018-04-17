# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapyredis.tool.screenshot_fdfs import FDFSClient

class RandomAgentMiddleWare(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self,crawler):
        self.ua = UserAgent()
        # 取到其定义的获取Useragent的方法
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):

        def getAgent():
            userAgent = getattr(self.ua,self.ua_type)
            print("=====设置代理userAgent:{0}".format(userAgent))
            return userAgent
        request.headers.setdefault(b'User-Agent', getAgent())
        request.headers.setdefault(b'Connection', 'keep-alive')

    def process_response(self, request, response, spider):
        # print(response.text)
        return response

class PhantomJSMiddleware(object):
    def __init__(self,crawler):
        self.ua = UserAgent()
        # 取到其定义的获取Useragent的方法
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")
        self.fdfs = FDFSClient()

        crawler.spider.logger.info("=========PhantomJS浏览器初始化！！！")

        def getAgent():
            userAgent = getattr(self.ua, self.ua_type)
            crawler.spider.logger.info("=====设置代理userAgent:{0}".format(userAgent))
            return userAgent

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (getAgent())

        self.webDriver = webdriver.PhantomJS(desired_capabilities=dcap)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # 详细处理页
        if len(spider.detailList)>=1:
            for detail in spider.detailList:
                if detail in request.url:
                    spider.logger.info("===========使用selenium下载")
                    self.webDriver.get(request.url)
                    content = self.webDriver.page_source.encode('utf-8')

                    # spider.logger.info("===========保存快照")
                    # screenshotData = self.webDriver.get_screenshot_as_png()
                    # screenshotUri = self.fdfs.save(screenshotData)
                    # request.meta['screenshot'] = screenshotUri

                    return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

    def process_response(self, request, response, spider):
        # print(response.text)
        return response


class ScrapyredisSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
