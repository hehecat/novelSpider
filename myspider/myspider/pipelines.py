# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib.error import HTTPError, URLError

from pymongo import MongoClient
from urllib import request
from bs4 import BeautifulSoup

class MyspiderPipeline(object):
    def process_item(self, item, spider):
        if "novel_section_urls" in item:
            # 获取Mongodb链接
            client = MongoClient('localhost', 27017)
            # 连接数据库
            db = client.novel
            # 获取小说名称
            novel_name = item['novel_name']
            # 根据小说名字，使用集合，没有则创建
            novel = db[novel_name]

            # 使用记录已抓取网页的集合，没有则创建
            section_url_downloaded_collection = db.section_url_collection

            index = 0
            print("正在下载：" + item["novel_name"])

            # 根据小说每个章节的地址，下载小说各个章节
            for section_url in item['novel_section_urls']:
                # 根据对应关系，找出章节名称
                section_name = item["section_url_And_section_name"][section_url]
                # 如果将要下载的小说章节没有在section_url_collection集合中，也就是从未下载过，执行下载
                # 否则跳过
                if not section_url_downloaded_collection.find_one({"url": section_url}):
                    # 使用requests

                    # result = requests.get(section_url)
                    # result.encoding = 'gbk'
                    # download_html = result.text
                    response = request.Request(url=section_url)
                    download_response = request.urlopen(response)
                    download_html = download_response.read().decode('gbk')

                    # 利用BeautifulSoup对HTML进行处理，截取小说内容
                    soup_texts = BeautifulSoup(download_html, 'lxml')
                    soup_find = soup_texts.find("dd", attrs={"id": "contents"})
                    try:
                        content = str(soup_find)
                        content = content.replace('顶点小说 Ｘ２３ＵＳ．ＣＯＭ更新最快', '')[24:-5]
                    except AttributeError:
                        print(section_url, "爬取失败")

                    else:
                        # 向Mongodb数据库插入下载完的小说章节内容
                        novel.insert({
                            "_id": section_url.split('/')[-1][:-5],
                            "novel_name": item['novel_name'],
                            "novel_family": item['novel_family'],
                            "novel_author": item['novel_author'],
                            "novel_status": item['novel_status'],
                            "section_name": section_name,
                            "content": content
                        })
                        index += 1
                        # 下载完成，则将章节地址存入section_url_downloaded_collection集合
                        section_url_downloaded_collection.insert({"url": section_url})

            print("下载完成：" + item['novel_name'])
            return item


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
        self.db.authenticate('novel', 'novel')

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
            "section_name": item['capture_name'],
            "content": item['capture_content']
        })
        section_url_downloaded_collection.insert({"url": url})
        return item