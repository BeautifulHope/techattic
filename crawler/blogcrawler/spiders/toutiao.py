# -*- coding: utf-8 -*-
import arrow
import scrapy
from ..items import BlogcrawlerItem

class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['toutiao.io']
    start_urls = [f'https://toutiao.io/posts/hot/90?page={n}' for n in range(1, 9)]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        "Connection": "keep-alive",
        "Host": "toutiao.io",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        now = arrow.now()
        items = response.css('.posts .post')
        for item in items:
            i = BlogcrawlerItem()
            i['title'] = item.css('h3.title a::attr(title)').extract_first()
            i['author'] = item.css('.subject-name a::text').extract_first()
            i['date'] = now.format('YYYY-MM-DD')
            i['source'] = 'https://toutiao.io' + item.css('h3.title a::attr(href)').extract_first()
            i['view'] = int(item.css('a.like-button span::text').extract_first())
            i['site'] = self.name
            yield i
