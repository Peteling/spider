# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy import Selector

from ..items import SteamItem
from ..utils.data_format import date_format, get_player, system_format
from ..utils.common import get_md5


class SteamSpider(scrapy.Spider):
    name = 'steam'
    allowed_domains = ['steampowered.com']
    start_urls = ['http://store.steampowered.com/search/?page=1']
    cookie = {'steamLogin': '',
              'birthtime': '',
              'lastagecheckage': '',
              'mature_content': ''}

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath("//div[@id='search_result_container']/div[2]//@href").extract()
        for link in links:
            yield Request(url=link, cookies=self.cookie, callback=self.parse_detail)

        PageList = range(2, 500)
        for i in PageList:
            url2 = 'http://store.steampowered.com/search/?page=' + str(i)
            yield Request(url2, callback=self.parse)

    def parse_detail(self, response):
        title = response.xpath("//div[@class='apphub_AppName']/text()").extract_first("")
        url = response.xpath("//div[@class='block_content_inner']/div[2]/a/@href").extract_first("")
        release_date = response.xpath("//div[@class='release_date']/span/text()").extract_first("")
        rencent_responsive = response.xpath("//div[@class='summary column']/span[3]/text()").extract_first("").strip()
        summary_responsive = response.xpath("//div[@class='user_reviews_summary_row']/@data-store-tooltip").extract_first("")
        tags = response.xpath("//div[@class='glance_tags popular_tags']/a")
        user_tag = []
        for single_tag in tags:
            t = single_tag.xpath('text()').extract_first("").strip()
            user_tag.append(t)
        system = []
        systems = response.xpath("//div[@class='sysreq_tabs']/div")
        for sy in systems:
            s = sy.xpath("text()").extract_first("").strip()
            system.append(s)
        detail = response.xpath("//div[@class='block_content_inner']/div[1]/a")
        type = []
        for a in detail[:-2]:
            type.append(a.xpath("text()").extract_first(""))

        try:
            developer = detail[-2].xpath("text()").extract_first("")
        except Exception as e:
            print(e)
            developer = ""
        try:
            publisher = detail[-1].xpath("text()").extract_first("")
        except Exception as e:
            print(e)
            publisher = ""
        # developer_link = detail[-2].xpath("@href").extract_first("")
        # publisher_link = detail[-1].xpath("@href").extract_first("")

        player_num = get_player(summary_responsive, flag=1)
        summary_responsive = get_player(summary_responsive, flag=0)
        rencent_responsive = get_player(rencent_responsive, flag=0)
        system = system_format(system)
        id = get_md5(url)

        steamItem = SteamItem()
        steamItem['id'] = id
        steamItem['title'] = title
        steamItem['url'] = url
        steamItem['release_date'] = release_date
        steamItem['rencent_responsive'] = rencent_responsive
        steamItem['summary_responsive'] = summary_responsive
        steamItem['player_num'] = player_num
        steamItem['tags'] = user_tag
        steamItem['types'] = type
        steamItem['system'] = system
        steamItem['developer'] = developer
        steamItem['publisher'] = publisher
        yield steamItem


