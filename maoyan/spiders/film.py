# -*- coding: utf-8 -*-

from scrapy.xlib.pydispatch import dispatcher
import scrapy
from scrapy import signals
from scrapy.http import Request
from urllib import parse
from selenium import webdriver
from maoyan.items import MaoyanItemLoader, MaoyanFilmItem
from maoyan.utils.common import get_film_id


class FilmSpider(scrapy.Spider):
    name = "film"
    allowed_domains = ["maoyan.com"]
    start_urls = [
        'http://maoyan.com/films',
    ]

    def __init__(self):
        # self.driver = webdriver.PhantomJS(executable_path="G:\\phantomjs-2.1.1-windows\\bin\phantomjs.exe")
        self.fail_urls = []
        # super(FilmSpider, self).__init__()
        # dispatcher.connect(self.spider_close, signals.spider_closed)
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def spider_close(self, spider):
        print("spider closed")
        # self.driver.quit()

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("Failed_urls", ",".join(self.fail_urls))

    def parse(self, response):
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

        tag_urls = response.css(".tags li a::attr(href)").extract()[1:]
        for turl in tag_urls:
            yield Request(url=parse.urljoin(response.url, turl),
                          callback=self.parse)

        next_url = response.css(".list-pager li a::attr(href)").extract()
        if len(next_url) != 0 and "javascript" not in next_url[-1]:
            next = next_url[-1]
            yield Request(url=parse.urljoin(response.url, next),
                          callback=self.parse)

        items_url = response.css(".movie-list .movie-item a::attr(href)").extract()
        for item_url in items_url:
            yield Request(url=parse.urljoin(response.url, item_url),
                          callback=self.parse_detail)
        # yield Request(url='http://maoyan.com/films/345011', callback=self.parse_detail)

    def parse_detail(self, response):
        item_loader = MaoyanItemLoader(item=MaoyanFilmItem(), response=response)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_film_id(response.url))
        item_loader.add_css("title", ".movie-brief-container h3::text")
        item_loader.add_css("front_image_url", ".avater-shadow img::attr(src)")
        #item_loader.add_css("front_image_path")
        item_loader.add_css("score", ".pro-score span::text")
        item_loader.add_css("tags", ".movie-brief-container li:nth-child(1)::text")
        item_loader.add_css("screen_date", ".movie-brief-container li:nth-child(3)::text")
        item_loader.add_css("place", ".movie-brief-container li:nth-child(2)::text")
        item_loader.add_css("content", ".mod-content span[class='dra']::text")
        item_loader.add_css("actors", ".actor div a::text")
        item_loader.add_css("related_films", ".related-movies .channel-detail a::text")
        maoyan_item = item_loader.load_item()
        yield maoyan_item

