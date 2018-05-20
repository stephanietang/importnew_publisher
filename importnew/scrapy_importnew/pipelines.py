# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from pymongo import MongoClient
from collections import OrderedDict
from scrapy.conf import settings


class ScrapyImportnewPipeline(object):
    
    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

        # setting for mongoDB
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.posts = db[settings['MONGODB_COLLECTION']]

        result = self.posts.remove()
        print('Cleaned mongodb Collections', result)

    def process_item(self, item, spider):

    	# insert to json
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)

        # insert into mongodb
        post_id = self.posts.insert_one(item).inserted_id
        print("post_id = ", post_id)
        return item

    def close_spider(self, spider):
        self.file.close()
