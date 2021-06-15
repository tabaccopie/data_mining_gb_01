import scrapy

from .loaders import AvitoLoader
from .xpath_selectors import ADS


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['www.avito.ru']
    start_urls = ['https://www.avito.ru/moskva/nedvizhimost']

    def parse(self, response):
        yield response.follow(response.xpath("//a[@data-category-id='24'][@title='Все квартиры']/@href").get(),
                              callback=self.appartments_parse)

    def appartments_parse(self, response, paginate=True):
        for url in response.xpath(ADS["selector"]):
            yield response.follow(url, getattr(self, ADS["callback"]))

        for page_num in range(2, 101) if paginate else []:
            yield response.follow(f"?p={page_num}", callback=self.parse, cb_kwargs={"paginate": False})

    def ads_parse(self, response):
        loader = AvitoLoader(response=response)
        yield loader.load_item()