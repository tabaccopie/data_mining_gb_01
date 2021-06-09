LIST = {
    'pagination': '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
    'vacancy_urls': '//a[@data-qa="vacancy-serp__vacancy-title"]/@href',
}
VACANCY = {
    "title": '//h1[@data-qa="vacancy-title"]/text()',
    "salary": '//p[@class="vacancy-salary"]//text()',
    "description": '//div[@data-qa="vacancy-description"]//text()',
    "skills": '//div[@class="bloko-tag-list"]//span[@data-qa="bloko-tag__text"]/text()',
    "company_url": '//a[@data-qa="vacancy-company-name"]//@href',
}

COMPANY = {
    'name': '//h1/span[contains(@class, "company-header-title-name")]/text()',
    'url': '//a[contains(@data-qa, "company-site")]/@href',
    'description': '//div[contains(@data-qa, "company-description")]//text()',
    'areas': '//div[contains(@class, "employer-sidebar-block")]//p//text()',
    'vacancies_page': '//a[@data-qa="employer-page__employer-vacancies-link"]//@href',
}