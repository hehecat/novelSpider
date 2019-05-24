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
            mongo_db=crawler.settings.get('MONGO_DB_NAME', 'novel')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # mongodb 数据库账号密码认证
        # self.db.authenticate('x23us', 'x23us')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        url = item['capture_url']
        # 使用记录已抓取网页的集合，没有则创建
        section_url_downloaded_collection = self.db.section_url_collection

        # if not section_url_downloaded_collection.find_one({"url": url}):
        # 存小说章节内容
        novel = self.db[item['novel_name']]
        novel.insert({
            "_id": url.split('/')[-1][:-5],
            "section_name": item['capture_name'],
            "content": item['capture_content']
        })

        # 存小说信息
        novel_intro = self.db['novel']
        if not novel_intro.find_one({"novel_name": item['novel_name']}):
            novel_intro.insert({
                "novel_name": item['novel_name'].strip(),
                "novel_family": item['novel_family'].strip(),
                "novel_author": item['novel_author'].strip(),
                'novel_introduction': item['novel_introduction'].strip(),
                "novel_number": item['novel_number'].strip(),
                'novel_store': item['novel_store'].strip(),
                'novel_click': item['novel_click'].strip(),
                'novel_recommend': item['novel_recommend'].strip(),
                "novel_status": item['novel_status'].strip(),
                'novel_url': item['novel_url'].strip(),
                'novel_cover': item['novel_cover'].strip()

            })

        section_url_downloaded_collection.insert({"url": url})

        return item