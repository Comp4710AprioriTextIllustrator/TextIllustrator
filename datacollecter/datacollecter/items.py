# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DatacollecterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItem(scrapy.Item):
    text = scrapy.Field()
    images = scrapy.Field()

class ImageItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    file_name = scrapy.Field() #the name on disk... we should be downloading images
