import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from spiders.CBD import CBDSpider
from scrapy import signals
import json

configure_logging()
runner = CrawlerRunner()
result_file = open('result.json', 'w', encoding='utf-8')

def item_scraped(item):
    result_file.write(json.dumps(dict(item), ensure_ascii=False) + '\n')

@defer.inlineCallbacks
def crawl():
    runner.signals.connect(item_scraped, signal=signals.item_scraped)
    yield runner.crawl(CBDSpider, city='bj')
    result_file.close()
    reactor.stop()

crawl()
reactor.run()