# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pandas as pd
from redis import Redis
from scrapy.exceptions import DropItem

redis_db = Redis(host='localhost', port=6379, db=3)
redis_data_dict = 'k_url'


class BlogcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLPipeline(object):

    table_name = 'article'

    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST', 'localhost'),
            user = crawler.settings.get('MYSQL_USER', 'root'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            db = crawler.settings.get('MYSQL_DBNAME', 'techattic')
        )
    
    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
        self.cursor = self.conn.cursor()
        redis_db.flushdb()
        if redis_db.hlen(redis_data_dict) == 0:
            sql = f"SELECT source FROM {self.table_name}"
            df = pd.read_sql(sql, self.conn)
            for source in df['source'].get_values():
                redis_db.hset(redis_data_dict, source, 0)

    def close_spider(self, spider):
        self.conn.close()
    
    def process_item(self, item, spider):
        # 利用redis实现去重
        if redis_db.hexists(redis_data_dict, item['source']):
            raise DropItem(f"Duplicate item found: {item}")
        else:
            sql = f"INSERT INTO `{self.table_name}` (`title`, `author`, `date`, `source`, `view`, `site`) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (item['title'], item['author'], item['date'], item['source'], item['view'], item['site']))
            self.conn.commit()
