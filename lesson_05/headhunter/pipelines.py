# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .settings import BOT_NAME
from pymongo import MongoClient


class HeadhunterPipeline:
    def process_item(self, item, spider):
        return item


class HHMongoPipeline:

    def __init__(self):
        client = MongoClient()
        self.db = client[BOT_NAME]

    def process_item(self, item, spider):
        if 'title' in item.fields:
            collection = self.db[spider.name + "_vacancies"]
            collection.insert_one(item)
        else:
            collection = self.db[spider.name + "_companies"]
            collection.insert_one(item)
        return item