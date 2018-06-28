import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)

for spider in process.spiders.list():
    print(f'Running spider {spider}...')
    process.crawl(spider)
process.start()