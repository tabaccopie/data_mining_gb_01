import scrapy
import pymongo
import re

db = pymongo.MongoClient('mongodb://localhost:27017')['gb_parse_ayoula']['autoyoula_collection']


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']
    css_query = {
        'brands': '.TransportMainFilters_brandsList__2tIkv a.blackLink',
        'pagination': '.Paginator_block__2XAPy a.Paginator_button__u1e7D',
        'ads': 'a.SerpSnippet_name__3F7Yu.blackLink',
    }

    def _get_follow(self, response, selector_str, callback):
        for a_link in response.css(selector_str):
            url = a_link.attrib.get('href')
            yield response.follow(url, callback=callback)

    def parse(self, response):
        yield from self._get_follow(
            response,
            self.css_query['brands'],
            self.brand_parse
        )

    def brand_parse(self, response):
        yield from self._get_follow(
            response,
            self.css_query['pagination'],
            self.brand_parse
        )
        yield from self._get_follow(
            response,
            self.css_query['ads'],
            self.car_parse
        )

    def car_parse(self, response):
        data = {
            'title': response.css('.AdvertCard_advertTitle__1S1Ak::text').get(),
            'price': self.get_price(response),
            'images': [img.attrib.get('src') for img in response.css('figure.PhotoGallery_photo__36e_r img')],
            'description': response.css('div.AdvertCard_descriptionInner__KnuRi::text').get(),
            'url': response.url,
            'author': self.js_decoder_author(response),
            'specification': self.get_specifications(response),
        }

        print(data)
        db.insert_one(data)

    def get_specifications(self, response):
        specifications_result = {itm.css('.AdvertSpecs_label__2JHnS::text').get(): itm.css(
            '.AdvertSpecs_data__xK2Qx::text').get() or itm.css('a::text').get() for itm in
                                 response.css('.AdvertSpecs_row__ljPcX')}
        return specifications_result

    def get_price(self, response):
        result = response.css('div.AdvertCard_price__3dDCr::text').get()
        if result:
            result = float(result.replace("\u2009", ''))
            return result
        else:
            return None

    def js_decoder_author(self, response):
        script = response.css('script:contains("window.transitState = decodeURIComponent")::text').get()
        re_str = re.compile(r"youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar")
        result = re.findall(re_str, script)
        return f'https://youla.ru/user/{result[0]}' if result else None
