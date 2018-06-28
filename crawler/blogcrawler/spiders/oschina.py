# -*- coding: utf-8 -*-
import arrow
import scrapy
from ..items import BlogcrawlerItem

class OschinaSpider(scrapy.Spider):
    name = 'oschina'
    allowed_domains = ['www.oschina.net']
    start_urls = ['https://www.oschina.net/blog',
                  'https://www.oschina.net/blog?classification=428602',
                  'https://www.oschina.net/blog?classification=428612',
                  'https://www.oschina.net/blog?classification=5611447',
                  'https://www.oschina.net/blog?classification=428640',
                  'https://www.oschina.net/blog?classification=429511',
                  'https://www.oschina.net/blog?classification=428609',
                  'https://www.oschina.net/blog?classification=428610',
                  'https://www.oschina.net/blog?classification=428611',
                  'https://www.oschina.net/blog?classification=428647',
                  'https://www.oschina.net/blog?classification=428613',
                  'https://www.oschina.net/blog?classification=428638',
                  'https://www.oschina.net/blog?classification=5593654',
                  'https://www.oschina.net/blog?classification=428639',
                  'https://www.oschina.net/blog?classification=430884',
                  'https://www.oschina.net/blog?classification=430381', ]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        "Connection": "keep-alive",
        "Host": "www.oschina.net",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        now = arrow.now()
        items = response.css('.blog-list .item')
        for item in items:
            i = BlogcrawlerItem()
            title = item.css('header.blog-title-box a::attr(title)').extract_first()
            if title == ' ':
                title = '默认标题'
            i['title'] = title
            i['author'] = item.css('footer.blog-footer-box span::text').extract_first()
            i['date'] = now.format('YYYY-MM-DD')
            i['source'] = item.css('header.blog-title-box a::attr(href)').extract_first()
            try:
                i['view'] = int(item.css('footer.blog-footer-box span::text').extract()[3][3:])
            except IndexError:
                i['view'] = 0
            i['site'] = self.name
            yield i
