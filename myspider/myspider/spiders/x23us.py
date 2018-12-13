# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Selector
from ..items import MyspiderItem
from scrapy_redis.spiders import RedisSpider

class X23usSpider(RedisSpider):
    name = 'x23us'
    allowed_domains = ['x23us.com']

    # slave注释下面的start_urls  从redis获取
    start_urls = ['https://www.x23us.com/quanben/1']
    server_link = 'https://www.x23us.com/quanben/'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse1)

    # 获取总排行榜每个页面的链接
    def parse1(self, response):
        res = Selector(response)
        # 获取总排行榜小说页码数
        max_num = res.xpath('//*[@id="pagestats"]/text()').extract_first()
        max_num = max_num.split('/')[1]
        print("总排行榜最大页面数为：" + max_num)
        for i in range(1, int(max_num)):
            # 构造总排行榜中每个页面的链接
            print('获得排行榜', i)
            page_url = self.server_link + str(i)
            yield scrapy.Request(url=page_url, callback=self.parse2)

    # 访问总排行榜的每个页面
    def parse2(self, response):
        print(response.url)
        items = []
        res = Selector(response)
        # 获得页面上所有小说主页链接地址
        novel_urls = res.xpath('//table//td[1]/a[1]/@href').extract()
        # 获得页面上所有小说的名称
        novel_names = res.xpath('//table//tr/td[1]/a[2]/text()').extract()

        page_novel_number = len(novel_urls)
        for index in range(page_novel_number):
            item = MyspiderItem()
            item['novel_name'] = novel_names[index]
            item['novel_url'] = novel_urls[index]
            items.append(item)

        for item in items:
            # 访问每个小说主页,传递novel_name
            yield scrapy.Request(url=item['novel_url'], meta={'item': item}, callback=self.parse3)

    # 访问小说主页，继续完善item
    def parse3(self, response):

        item = response.meta['item']
        item['novel_family'] = response.xpath('//table//tr[1]/td[1]/a/text()').extract_first()
        item['novel_number'] = response.xpath('//table//tr[2]/td[2]/text()').extract_first()
        item['novel_click'] = response.xpath('//table//tr[3]/td[1]/text()').extract_first()
        item['novel_recommend'] = response.xpath('//table//tr[4]/td[1]/text()').extract_first()
        item['novel_store'] = response.xpath('//table//tr[2]/td[1]/text()').extract_first()
        item['novel_author'] = response.xpath('//table[@id="at"]//tr[1]/td[2]/text()').extract_first()
        item['novel_status'] = response.xpath('//table//tr[1]/td[3]/text()').extract_first()
        item['novel_updatetime'] = response.xpath('//table//tr[2]/td[3]/text()').extract_first()
        intro_xpath = response.xpath('//dl[@id="content"]/dd[2]//p[2][not(@class)]')[0]
        item['novel_introduction'] = intro_xpath.xpath('string(.)').extract_first()

        url = response.xpath('//a[@class="read"]/@href').extract_first()

        yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse4)

    # 获得小说所有章节的地址和名称
    def parse4(self, response):
        item = response.meta['item']

        section_urls = response.xpath('//table//tr/td/a/@href').extract()
        section_urls = list(map(lambda x: response.url + x, section_urls))
        for url in section_urls:
            item['capture_url'] = url
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse5)

    # 访问小说章节页，获取小说内容
    def parse5(self, response):
        # 接收传递的item
        item = response.meta['item']
        content = response.css('#contents').extract_first()[20:-5]
        title = response.xpath('//*[@id="amain"]/dl/dd[1]/h1/text()').extract_first()
        item['capture_content'] = content.replace('顶点小说 Ｘ２３ＵＳ．ＣＯＭ更新最快','')
        item['capture_name'] = title
        yield item

