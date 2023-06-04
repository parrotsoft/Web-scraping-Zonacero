from bs4 import BeautifulSoup
import requests
import hashlib


class Cryptographic:
    def __init__(self):
        pass

    def get_fingerprint(self, text):
        cadena_bytes = text.encode('utf-8')
        sha256_hash = hashlib.sha256(cadena_bytes)
        fingerprint = sha256_hash.hexdigest()

        return fingerprint


class Article:
    def __int__(self, title, date, category, link):
        self.title = title
        self.date = date
        self.category = category
        self.link = link


class Request:
    def __init__(self, _url):
        self.url = _url

    def get_soup(self):
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        return soup


if __name__ == '__main__':
    url = 'https://zonacero.com'

    crypt = Cryptographic()

    zonacero = Request(url)
    soup = zonacero.get_soup()

    titles = soup.select('.views-field-title')
    data = list()

    for title in titles:
        link = url + title.find('a')['href']
        news = Request(link)
        soup2 = news.get_soup()

        tags = soup2.find('div', class_='views-field-field-tags')
        if tags != None:
            tags = tags.find_all('a')
            tags_end = list()
            for tag in tags:
                tags_end.append(tag.text)

        date = soup2.select('.time-authored-on')
        if len(date) > 0:
            date = date[0].text

        category = soup2.select('.news-intern-category')
        if len(category) > 0:
            category = category[0].text

        banner = soup2.find('div', class_='field--type-image')
        if len(banner) > 0:
            banner = url + banner.find('img')['src']

        fingerprint = crypt.get_fingerprint(title.text)

        data.append([title.text, link, date, category, banner, tags_end, fingerprint])

    print(data)
