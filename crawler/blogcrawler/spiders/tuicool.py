# -*- coding: utf-8 -*-
import arrow
import scrapy
from ..items import BlogcrawlerItem

class TuicoolSpider(scrapy.Spider):
    name = 'tuicool'
    allowed_domains = ['www.tuicool.com']
    start_urls = [f'https://www.tuicool.com/ah/0/{n}?lang={m}' for n in range(1, 21) for m in [1, 2]]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        "Connection": "keep-alive",
        "Host": "www.tuicool.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        now = arrow.now()
        items = response.css('.list_article .list_article_item')
        for item in items:
            i = BlogcrawlerItem()
            i['title'] = item.css('.title a::attr(title)').extract_first()
            i['author'] = item.css('.tip span::text').extract_first().strip()
            date = item.css('.tip span::text').extract()[2].strip()
            date = str(now.year) + '-' + date
            i['date'] = date[:-6]
            i['source'] = 'https://www.tuicool.com' + item.css('.title a::attr(href)').extract_first()
            i['view'] = 0
            i['site'] = self.name
            yield i
