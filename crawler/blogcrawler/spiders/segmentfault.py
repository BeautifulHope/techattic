# -*- coding: utf-8 -*-
import re
import arrow
import scrapy
from ..items import BlogcrawlerItem

class SegmentfaultSpider(scrapy.Spider):
    name = 'segmentfault'
    allowed_domains = ['segmentfault.com']
    start_urls = [f'https://segmentfault.com/blogs?page={n}' for n in range(1, 799)]

    def parse(self, response):
        now = arrow.now()
        items = response.css('.stream-list section')
        for item in items:
            i = BlogcrawlerItem()
            i['title'] = item.css('h2.title a::text').extract_first()
            i['author'] = item.css('ul.author span a::text').extract_first()
            date = item.css('ul.author span::text').extract_first().strip().split('\n')[0]
            if '小时' in date:
                i['date'] = now.format('YYYY-MM-DD')
            elif '天' in date:
                timedelta = int(date[:-3])
                i['date'] = now.shift(days=-timedelta).format('YYYY-MM-DD')
            elif '月' in date and '日' in date and not '年' in date:
                date = re.sub('月|日', '-', date)[:-1]
                year = str(now.year)
                month, day = date.split('-')
                if int(month) < 10:
                    month = '0' + month
                if int(day) < 10:
                    day = '0' + day
                i['date'] = '-'.join([year, month, day])
            else:
                i['date'] = re.sub('年|月|日', '-', date)[:-1]
            i['source'] = 'https://segmentfault.com'+ item.css('h2.title a::attr(href)').extract_first()
            i['view'] = int(item.css('.stream__item-zan-number::text').extract_first())
            i['site'] = self.name
            yield i
