from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from headhunter.spiders.hhspider import HhspiderSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule("headhunter.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(HhspiderSpider)
    crawler_process.start()
