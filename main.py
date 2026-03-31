import requests
import bs4
from fake_headers import Headers

## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# Функция для получения текста страницы
def get_page(page_url :str) -> str:
     headers = Headers(browser='chrome', os='win').generate()
     try:
          response = requests.get(page_url, headers=headers, verify=False)
          return response.text
     except Exception:
          raise Exception

# Функция проверки наличия ключевых слов
def is_relevant(text :str) -> bool:
     return any(word in text.lower() for word in KEYWORDS)


## Основной код
url = 'https://habr.com/ru/articles/'
try:
     page = get_page(url)
except Exception as e:
     print(f'Ошибка получения списка статей: {e}')
     exit(1)

soup = bs4.BeautifulSoup(page, features='lxml')

article_block = soup.select_one('div.tm-articles-list')
if article_block:
     articles_list = article_block.select('article.tm-articles-list__item')
else:
     print(f'Блок со статьями не найден на странице')
     exit(1)

if articles_list:
     for article in articles_list:
          text_preview = article.select_one('div.article-formatted-body.article-formatted-body.article-formatted-body_version-2').text
          title = article.select_one('h2').text.strip()
          link = 'https://habr.com' + article.select_one('a.readmore')['href']
          time = article.select_one('time')['title']
          # Лезем внутрь статьи и разбираем ее текст
          try:
               article_page = get_page(link)
          except Exception as e:
               print(f'Не удалось получить текст статьи: {title}. Ошибка: {e}')
               continue
          article_soup = bs4.BeautifulSoup(article_page, features='lxml')
          text_article = article_soup.select_one('div.article-body').text
          # Проверяем наличие ключевых слов в заголовке и тексте превью
          if  is_relevant(text_preview) or is_relevant(title) or is_relevant(text_article):
               print(f'{time} – {title} – {link}')

else:
     print(f'Не найдены статьи')
     exit(1)



