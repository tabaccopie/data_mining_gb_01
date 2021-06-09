import scrapy
from .xpath_selectors import LIST, VACANCY, COMPANY
from ..loaders import HHVacancyLoader, HHCompanyLoader


class HhspiderSpider(scrapy.Spider):
    name = 'hhspider'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def parse(self, response, **kwargs):
        for pag_page in response.xpath(LIST['pagination']):
            yield response.follow(pag_page, callback=self.parse)

        for vacancy_page in response.xpath(LIST['vacancy_urls']):
            yield response.follow(vacancy_page, callback=self.vacancy_parse)

    def vacancy_parse(self, response, **kwargs):
        loader = HHVacancyLoader(response=response)
        loader.add_value('url', response.url)
        for key, value in VACANCY.items():
            loader.add_xpath(key, value)

        yield loader.load_item()
        yield response.follow(response.xpath(VACANCY['company_url']).get(), callback=self.company_parse)

    def company_parse(self, response, **kwargs):
        loader = HHCompanyLoader(response=response)
        for key, value in COMPANY.items():
            loader.add_xpath(key, value)

        yield loader.load_item()
        resp = response.xpath(COMPANY['vacancies_page']).get()
        if resp:
            yield response.follow(resp, callback=self.companies_vacancies_pages_parse)

    def companies_vacancies_pages_parse(self, response, **kwargs):
        if response:
            for pag_page in response.xpath(LIST['pagination']):
                yield response.follow(pag_page, callback=self.companies_vacancies_pages_parse)

            for vacancy_page in response.xpath(LIST['vacancy_urls']):
                yield response.follow(vacancy_page, callback=self.companies_vacancy_parse)
        else:
            yield HHVacancyLoader(response=response)

    def companies_vacancy_parse(self, response, **kwargs):
        loader = HHVacancyLoader(response=response)
        loader.add_value('url', response.url)
        for key, value in VACANCY.items():
            loader.add_xpath(key, value)

        yield loader.load_item()
