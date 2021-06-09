# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HeadhunterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HHVacancyItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    company_url = scrapy.Field()


class HHCompanyItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    areas = scrapy.Field()
    vacancies_page = scrapy.Field()