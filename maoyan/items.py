# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import hashlib

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from maoyan.utils.common import date_converts, get_place, return_value


class MaoyanItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class MaoyanFilmItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value),
    )
    front_image_path = scrapy.Field()
    score = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(",")
    )
    screen_date = scrapy.Field(
        input_processor=MapCompose(date_converts),
    )
    place = scrapy.Field(
        input_processor=MapCompose(get_place),
    )
    content = scrapy.Field()
    actors = scrapy.Field(
        output_processor=Join(",")
    )
    related_films = scrapy.Field(
        output_processor=Join(",")
    )

    def get_insert_sql(self):
        insert_sql = """
                    insert into movie_msg(url, url_object_id, title, front_image_url,
                                          front_image_path, score, tags, screen_date,
                                          place, content, actors, related_films)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        params = (self['url'], self['url_object_id'], self['title'],
                  self['front_image_url'][0], " ",
                  self['score'], self['tags'], self['screen_date'],
                  self['place'], self['content'], self['actors'],
                  self['related_films'])
        return insert_sql, params


class SteamItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    release_date = scrapy.Field()
    rencent_responsive = scrapy.Field()
    summary_responsive = scrapy.Field()
    player_num = scrapy.Field()
    tags = scrapy.Field()
    types = scrapy.Field()
    system = scrapy.Field()
    developer = scrapy.Field()
    publisher = scrapy.Field()


class AmazonSpiderItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    packed = scrapy.Field()
    comments_num = scrapy.Field()
    price = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO amazon_book (id, url, name, packed, comments_num, price)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        book_id = self.hash_book_id(self['name'] + self['packed'])
        url = self['url']
        name = self['name']
        packed = self['packed']
        comments_num = self['comments_num']
        price = self['price']
        params = (book_id, url, name, packed, comments_num, price)

        return insert_sql, params

    def hash_book_id(self, book_id):
        md5 = hashlib.md5()
        md5.update(book_id.encode('utf-8'))
        return md5.hexdigest()