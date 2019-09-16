# -*- coding: utf-8 -*-
import scrapy


class TestBaseSpider(scrapy.Spider):
    name = "test_base"
    allowed_domains = ["www.baidu.com"]
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
