import typing
import time
import requests
from urllib.parse import urljoin
import bs4
import pymongo
import datetime


class GbBlogParse:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) "
                      "Gecko/20100101 Firefox/88.0"
    }
    __parse_time = 0

    def __init__(self, start_url, db, delay=1.0):
        self.start_url = start_url
        self.db = db
        self.delay = delay
        self.done_urls = set()
        self.tasks = []
        self.tasks_creator({self.start_url, }, self.parse_feed)

    def _get_response(self, url):
        while True:
            next_time = self.__parse_time + self.delay
            if next_time > time.time():
                time.sleep(next_time - time.time())
            response = requests.get(url, headers=self.headers)
            print(f"RESPONSE: {response.url}")
            self.__parse_time = time.time()
            if response.status_code == 200:
                return response

    def get_task(self, url: str, callback: typing.Callable) -> typing.Callable:
        def task():
            response = self._get_response(url)
            return callback(response)

        return task

    def tasks_creator(self, urls: set, callback: typing.Callable):
        urls_set = urls - self.done_urls
        for url in urls_set:
            self.tasks.append(
                self.get_task(url, callback)
            )
            self.done_urls.add(url)

    def run(self):
        while True:
            try:
                task = self.tasks.pop(0)
                task()
            except IndexError:
                break

    def parse_feed(self, response: requests.Response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        ul_pagination = soup.find('ul', attrs={"class": "gb__pagination"})
        pagination_links = set(
            urljoin(response.url, itm.attrs.get('href'))
            for itm in ul_pagination.find_all('a') if
            itm.attrs.get("href")
        )
        self.tasks_creator(pagination_links, self.parse_feed)
        post_wrapper = soup.find("div", attrs={"class": "post-items-wrapper"})
        self.tasks_creator(
            set(
                urljoin(response.url, itm.attrs.get('href'))
                for itm in post_wrapper.find_all("a", attrs={"class": "post-item__title"}) if
                itm.attrs.get("href")
            ),
            self.parse_post
        )

    def _get_comments(self, post_id):
        api_path = f"/api/v2/comments?commentable_type=Post&commentable_id={post_id}&order=desc"
        response = self._get_response(urljoin(self.start_url, api_path))
        return response.json()

    def parse_post(self, response: requests.Response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        author_name_tag = soup.find('div', attrs={"itemprop": "author"})
        blogpost_content = soup.find('div', attrs={"class": "blogpost-content"})
        try:
            img_src = blogpost_content.find("img")["src"]
        except TypeError:
            img_src = "None"
        blogpost_datetime = soup.find('div', attrs={'class': 'blogpost-date-views'})
        post_datetime = datetime.datetime.fromisoformat(blogpost_datetime.find('time')['datetime'])
        # post_datetime = datetime.datetime.strptime(blogpost_datetime.find('time')['datetime'], '%Y-%m-%dT%H:%M:%S%z')
        comments_json = self._get_comments(soup.find("comments").attrs.get("commentable-id"))

        # создадим словарь из авторов и комментариев
        comments_dict = {}
        for comment in comments_json:
            tmp_dict = comment["comment"]
            comments_dict[f'{(tmp_dict["user"])["full_name"]}'] = tmp_dict["body"]

        # формируем датасет для записи в бд
        data = {
            'url': response.url,  # урл страницы материала
            "title": soup.find('h1', attrs={'class': "blogpost-title"}).text,  # заголовок материала
            "image link": img_src,  # Первое изображение материала (Ссылка)
            "post datetime": post_datetime,  # Дата публикации (в формате datetime)
            "author": {
                'name': author_name_tag.text,  # имя автора материала
                'url': urljoin(response.url, author_name_tag.parent.attrs["href"])  # ссылка на страницу автора
            },
            # комментарии в виде Автор: комментарий
            'comments': comments_dict
        }
        self._save(data)

    def _save(self, data: dict):
        collection = self.db["gb_blog_parse"]
        collection.insert_one(data)


if __name__ == '__main__':
    client_db = pymongo.MongoClient("mongodb://localhost:27017")
    db = client_db["gb_parse_ilyak"]
    parser = GbBlogParse("https://gb.ru/posts", db)
    parser.run()
