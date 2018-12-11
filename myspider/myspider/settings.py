# -*- coding: utf-8 -*-

# Scrapy settings for myspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'myspider'

SPIDER_MODULES = ['myspider.spiders']
NEWSPIDER_MODULE = 'myspider.spiders'

# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Don't cleanup redis queues, allows to pause/resume crawls.
# 不清理redis 可以断点续爬
SCHEDULER_PERSIST = True

# mongodb 数据库设置
MONGO_DB_URI = 'mongodb://ip_address:27017'
MONGO_DB_NAME = 'novel'

# redis设置
REDIS_URL = 'redis://root:password@ip_address:6379'

# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
# REDIS_PARAMS = {'password': 'pass'}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'myspider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    # 'myspider.pipelines.MyspiderPipeline': 300,
    'myspider.pipelines.MongoDBPipeline': 300,

}

DOWNLOAD_DELAY = 0
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 100

COOKIES_ENABLED = False
