import requests
from bs4 import BeautifulSoup

def get_article_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', class_='title').text.strip()
    author = soup.find('span', class_='byline-author').text.strip()
    published_at = soup.find('time', class_='published').text.strip()

    return {
        'title': title,
        'author': author,
        'published_at': published_at
    }

url = "https://medium.com/@coldstart_coder/basics-of-the-walrus-operator-in-python-a9b18ca1469c"
article_info = get_article_info(url)

print("Title:", article_info['title'])
print("Author:", article_info['author'])
print("Published at:", article_info['published_at'])
