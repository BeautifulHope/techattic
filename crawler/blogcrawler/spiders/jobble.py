# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import BlogcrawlerItem

class JobbleSpider(scrapy.Spider):
    name = 'jobble'
    allowed_domains = ['blog.jobbole.com']
    start_urls = [f'http://python.jobbole.com/all-posts/page/{n}/' for n in range(1, 83)]

    def parse(self, response):
        items = response.css('.post')
        for item in items:
            i = BlogcrawlerItem()
            i['title'] = item.css('.archive-title::attr(title)').extract_first()
            i['author'] = ''
            date = item.css('p').re_first('\d+\/\d+\/\d+')
            i['date'] = re.sub(r'/', '-', date)
            i['source'] = item.css('.archive-title::attr(href)').extract_first()
            i['view'] = 0
            i['site'] = self.name
            yield i
