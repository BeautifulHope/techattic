# -*- coding: utf-8 -*-
import scrapy
from ..items import BlogcrawlerItem

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['www.cnblogs.com']
    start_urls = [f'https://www.cnblogs.com/sitehome/p/{n}' for n in range(1, 201)]

    def parse(self, response):
        items = response.css('.post_item')
        for item in items:
            i = BlogcrawlerItem()
            i['title'] = item.css('.titlelnk::text').extract_first()
            i['author'] = item.css('.post_item_foot a::text').extract_first()
            i['date'] = item.css('.post_item_foot').re_first('发布于.*?\\r\\n').strip()[4:][:-6]
            i['source'] = item.css('.titlelnk::attr(href)').extract_first()
            i['view'] = int(item.css('.article_view a::text').re_first('\d+'))
            i['site'] = self.name
            yield i
