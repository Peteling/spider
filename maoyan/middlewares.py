# -*- coding: utf-8 -*-
__author__ = 'lateink'

from fake_useragent import UserAgent
from scrapy.http import HtmlResponse
from maoyan.utils.crawl_xici_ip import GetIP


class RandomUserAgentMiddlware(object):
    # 随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        print(get_ua())
        request.headers.setdefault('User-Agent', get_ua())


class RandomProxyMiddleware(object):
    #动态设置ip代理
    def process_request(self, request, spider):
        get_ip = GetIP()
        request.meta["proxy"] = get_ip.get_random_ip()


class JSPageMiddleware(object):
    # 通过PhantomJS请求动态网页
    def process_request(self, request, spider):
        if spider.name == "film":
            spider.browser.get(request.url)
            import time
            time.sleep(3)
            print("访问:{0}".format(request.url))
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)
