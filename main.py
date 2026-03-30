import requests
import bs4
from fake_headers import Headers

## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

## Основной код
url = 'https://habr.com/ru/articles'
headers = Headers(browser='chrome', os='win').generate()
response = requests.get(url, headers=headers)

soup = bs4.BeautifulSoup(response.text, features='lxml')

article_block = soup.select_one('div.tm-articles-list')
articles_list = article_block.select('article.tm-articles-list__item')

for article in articles_list:
     if any(word in article.text.lower() for word in KEYWORDS):
          title = article.select_one('h2').text.strip()
          time = article.select_one('time')['title']
          link = url + article.select_one('a.readmore')['href']
          print(f'{time} – {title} – {link}')


