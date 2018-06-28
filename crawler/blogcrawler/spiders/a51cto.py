# -*- coding: utf-8 -*-
import arrow
import scrapy
from ..items import BlogcrawlerItem

class A51ctoSpider(scrapy.Spider):
    name = '51cto'
    allowed_domains = ['www.51cto.com']
    start_urls = [f'http://blog.51cto.com/artcommend/p{n}' for n in range(1, 501)]

    def parse(self, response):
        now = arrow.now()
        items = response.css('ul.artical-list li')
        for item in items:
            i = BlogcrawlerItem()
            i['title'] = item.css('a.tit::text').extract_first()
            i['author'] = item.css('a.name::text').extract_first()
            date = item.css('p.time::text').extract_first()[4:]
            if '小时' in date:
                i['date'] = now.format('YYYY-MM-DD')
            elif '天' in date:
                timedelta = int(date[:-3])
                i['date'] = now.shift(days=-timedelta).format('YYYY-MM-DD')
            else:
                i['date'] = date[:-9]
            i['source'] = item.css('a.tit::attr(href)').extract_first()
            i['view'] = int(item.css('.bot span').re_first('\d+'))
            i['site'] = self.name
            yield i
