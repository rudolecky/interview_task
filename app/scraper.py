
import json
import re
from scrapy import signals, Spider
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from database import Db

class SrealitySpider(Spider):
    name = 'flat_sales'
    number_of_records = 500
    start_urls = [f'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page={number_of_records}']

    def parse(self, response):
        json_response = json.loads(response.body)
        for flat in json_response.get('_embedded').get('estates'):
            item = {}
            item['title'] = re.sub(r'\s', ' ', flat.get('name'))
            item['url'] = flat.get('_links').get('images')[0].get('href')
            yield item


results = []
def dispatch(item):
    results.append(item)

def scrape_into_db():
    db = Db()
    db.create_db()
    dispatcher.connect(dispatch, signal=signals.item_scraped)

    runner = CrawlerRunner()
    runner.crawl(SrealitySpider)
    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run(installSignalHandlers=0)

    db.insert(results)
    return db.select()

if __name__ == '__main__': 
    print(scrape_into_db())