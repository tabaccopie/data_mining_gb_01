from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoparser.spiders.avito import AvitoSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule("avitoparser.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(AvitoSpider)
    crawler_process.start()
