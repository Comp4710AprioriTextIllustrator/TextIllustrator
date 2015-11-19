# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo

logger = logging.getLogger(__name__)

class DatacollecterPipeline(object):
    collection_name = "articles"

    def __init__(self, mongo_uri, mongo_db):
        self.__mongo_uri = mongo_uri
        self.__mongo_db = mongo_db
        
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.__mongo_uri)
        self.db = self.client[self.__mongo_db]
        
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if self.client != None:
            logger.info("Inserting story '{story_title}' from spider '{spider_name}' into mongodb.".format(story_title=item['title'], spider_name=spider.name))
            self.db[self.collection_name].insert(dict(item))
        return item
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get("MONGO_URI"),
            mongo_db = crawler.settings.get("MONGO_DB")
        )
