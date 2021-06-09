from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from .items import HHVacancyItem, HHCompanyItem


class HHVacancyLoader(ItemLoader):
    default_item_class = HHVacancyItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    salary_in = ''.join
    salary_out = TakeFirst()


class HHCompanyLoader(ItemLoader):
    default_item_class = HHCompanyItem
    name_out = TakeFirst()
    url_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    areas = TakeFirst()
    vacancies_page = TakeFirst()