"""Задача организовать сбор данных, необходимо иметь метод сохранения данных в .json файлы результат: Данные
скачиваются с источника, при вызове метода/функции сохранения в файл скачанные данные сохраняются в Json вайлы,
для каждой категории товаров должен быть создан отдельный файл и содержать товары исключительно соответсвующие данной
категории. пример структуры данных для файла: нейминг ключей можно делать отличным от примера

{
"name": "имя категории",
"code": "Код соответсвующий категории (используется в запросах)",
"products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
}
"""

import json
import time
from pathlib import Path
import requests


class Parse5ka:
    headers = {
        "User-Agent": "NCSA_Mosaic/2.0 (Windows 3.1)"
    }

    def __init__(self, start_url, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url):
            file_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, file_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data['results']:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


# создаем новый класс парсинга категорий, наследуем от Parse5ka
class ParseCategories(Parse5ka):
    def __init__(self, start_url: str, categories_start_url: str, result_path: Path):
        super().__init__(start_url, result_path)
        self.categories_start_url = categories_start_url

    def parse_categories(self, url: str) -> list:
        response = self._get_response(url)
        return response.json()

    def run(self):
        for category in self.parse_categories(self.categories_start_url):
            products = self._parse(f"{self.start_url}?categories={category['parent_group_code']}")
            list_of_products = []
            for product in products:
                list_of_products.append(product)

            data = {
                "name": category['parent_group_name'],
                "code": category['parent_group_code'],
                "products": list_of_products  # список словарей товаров, соответствующих данной категории
            }
            file_path = self.save_path.joinpath(f"{category['parent_group_code']}.json")
            self._save(data, file_path)


def get_save_path(dir_name: str) -> Path:
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == '__main__':
    categories_url = "https://5ka.ru/api/v2/categories/"
    product_url = "https://5ka.ru/api/v2/special_offers/"
    # product_path = get_save_path('products')
    # parser = Parse5ka(product_url, product_path)
    # parser.run()
    categories_path = get_save_path('categories')
    parser_categories = ParseCategories(product_url, categories_url, categories_path)
    parser_categories.run()
