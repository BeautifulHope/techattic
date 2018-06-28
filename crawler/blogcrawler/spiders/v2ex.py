# -*- coding: utf-8 -*-
import arrow
import json
import scrapy
from ..items import BlogcrawlerItem

class V2exSpider(scrapy.Spider):
    name = 'v2ex'
    allowed_domains = ['www.v2ex.com']
    start_urls = ['https://www.v2ex.com/api/topics/latest.json']

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        for d in data:
            i = BlogcrawlerItem()
            i['title'] = d['title']
            i['author'] = d['member']['username']
            i['date'] = arrow.get(d['last_modified']).format('YYYY-MM-DD')
            i['source'] = d['url']
            i['view'] = int(d['replies'])
            i['site'] = self.name
            yield i