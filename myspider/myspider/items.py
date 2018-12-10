# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 小说名字
    novel_name = scrapy.Field()
    # 小说类别
    novel_family = scrapy.Field()
    # 小说主页地址
    novel_url = scrapy.Field()
    # 小说作者
    novel_author = scrapy.Field()
    # 小说状态
    novel_status = scrapy.Field()
    # 小说字数
    novel_number = scrapy.Field()

    # 章节内容
    capture_content = scrapy.Field()
    # 章节名
    capture_name = scrapy.Field()
    #章节地址
    capture_url = scrapy.Field()

    # # 小说所有章节页面
    # novel_all_section_url = scrapy.Field()
    # 小说最后更新时间
    novel_updatetime = scrapy.Field()

    # # 存放小说的章节地址，程序中存放的是一个列表
    # novel_section_urls = scrapy.Field()
    # # 存放小说的章节地址和小说章节名称的对应关系，程序中存储的是一个字典
    # section_url_And_section_name = scrapy.Field()


