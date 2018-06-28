# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import BlogcrawlerItem

class InfoqSpider(scrapy.Spider):
    name = 'infoq'
    allowed_domains = ['www.infoq.com']
    pages = [1, *[12*n for n in range(1, 343)]]
    start_urls = [f'http://www.infoq.com/cn/articles/{p}' for p in pages]

    def parse(self, response):
        subitems1 = response.css('.news_type1')
        subitems2 = response.css('.news_type2')
        items = [*subitems1, *subitems2]
        for item in items:
            i = BlogcrawlerItem()
            i['title'] = item.css('h2 a::attr(title)').extract_first()
            i['author'] = item.css('a.editorlink::text').extract_first()
            date = item.css('span.author').re_first('\d+年\d+月\d+日')
            date = re.sub(r'年|月|日', '-', date)[:-1]
            year, month, day = date.split('-')
            if int(month) < 10:
                month = '0' + month
            if int(day) < 10:
                day = '0' + day
            i['date'] = '-'.join([year, month, day])
            i['source'] = 'http://www.infoq.com' + item.css('h2 a::attr(href)').extract_first()
            i['view'] = 0
            i['site'] = self.name
            yield i
