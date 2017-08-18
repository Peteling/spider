# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from maoyan.items import AmazonSpiderItem


class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    start_urls = [
        "https://www.amazon.cn/gp/search/other/ref=sr_sa_p_lbr_one_browse-bin?rh=n%3A658390051%2Cn%3A%21658391051%2Cn"
        "%3A658394051%2Cp_6%3AA1AJ19PSB66TGU%2Cp_n_binding_browse-bin%3A2038564051&bbn=658394051&pickerToList"
        "=lbr_one_browse-bin&ie=UTF8&qid=1496321636",
        "https://www.amazon.cn/gp/search/other/ref=sr_sa_p_lbr_one_browse-bin?rh=n%3A658390051%2Cn%3A%21658391051%2Cn"
        "%3A658394051%2Cp_n_binding_browse-bin%3A2038565051&bbn=658394051&pickerToList=lbr_one_browse-bin&ie=UTF8&qid"
        "=1496321894"
    ]

    nextPage_xpath = '//a[@id="pagnNextLink"]'
    rules = (
        Rule(LinkExtractor(restrict_xpaths=(nextPage_xpath,)), follow=True, callback="parse_search_result"),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_starturls)

    def parse_starturls(self, response):
        url_list = response.xpath('//li/span[@class="a-list-item"]/a/@href').extract()
        home_url = "https://www.amazon.cn"
        url_list = [home_url + u for u in url_list]
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_search_result)

    def parse_search_result(self, response):
        result = response.xpath('//div[contains(@class, "a-fixed-left-grid-col a-col-right")]')
        for res in result:
            name = res.xpath('div[@class="a-row a-spacing-small"]/div/a/@title').extract()[0]
            url = res.xpath('div[@class="a-row a-spacing-small"]/div/a/@href').extract()[0]

            packed = res.xpath('div[@class="a-row"]/div[@class="a-column a-span7"]/div/a/h3/text()').extract()[0]
            price = res.xpath('div[@class="a-row"]/div[@class="a-column a-span7"]/div/a/span/text()').extract()[0]
            if price:
                price = float(price.replace("￥", ''))
            else:
                price = 0
            comments_list = res.xpath('div[@class="a-row"]/div[@class="a-column a-span5 a-span-last"]/div/a/text()').re(
                r'\d+')
            comments_num = "".join(comments_list)
            if comments_num:
                comments_num = int(comments_num)
            else:
                comments_num = 0

            AmazonItem = AmazonSpiderItem()
            AmazonItem['url'] = url
            AmazonItem['name'] = name
            AmazonItem['packed'] = packed
            AmazonItem['comments_num'] = comments_num
            AmazonItem['price'] = price
            yield AmazonItem
