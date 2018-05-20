# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyImportnewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    view = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    original_url = scrapy.Field()