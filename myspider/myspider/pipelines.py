# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib.error import HTTPError, URLError

from pymongo import MongoClient


class MongoDBPipeline(object):
    """
    将item写入MongoDB
    """

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_DB_URI', 'mongodb://localhost:27017'),
            mongo_db=crawler.settings.get('MONGO_DB_NAME', 'novel3')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # mongodb 数据库账号密码认证
        # self.db.authenticate('novel', 'novel')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        url = item['capture_url']
        # 使用记录已抓取网页的集合，没有则创建
        section_url_downloaded_collection = self.db.section_url_collection

        # if not section_url_downloaded_collection.find_one({"url": url}):
        novel = self.db[item['novel_name']]
        novel.insert({
            "_id": url.split('/')[-1][:-5],
            "novel_name": item['novel_name'],
            "novel_family": item['novel_family'],
            "novel_author": item['novel_author'],
            "novel_status": item['novel_status'],
            "novel_status": item['novel_status'],
            "novel_status": item['novel_status'],
            "novel_status": item['novel_status'],
            "section_name": item['capture_name'],
            "content": item['capture_content']
        })
        section_url_downloaded_collection.insert({"url": url})
        return item