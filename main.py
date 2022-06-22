import requests
from bs4 import BeautifulSoup
from requests.api import head
import time
from random import randrange
import json


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
}


def get_article_urls(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    pagination_count = int(soup.find('div', class_='pager').find_all('a')[-2].text)

    articles_url_list = []
    num = 0
    for page in range(1, pagination_count + 1):
    # for page in range(1, 2):
        response = s.get(url=f'https://gamebomb.ru/games?page={page}', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        article_urls = soup.find_all('h3')

        # print(article_urls)
        for au in article_urls:
            num += 1
            articles_url_list.append(f'{str(num)} {au.find("a").get("href")}')

        time.sleep(randrange(2, 5))
        print(f'Обработал {page}/{pagination_count}')

    with open('articles_description.txt', 'w', encoding='utf8') as f:
        for url in articles_url_list:
            f.write(f'{url}\n')

    return 'Работа по сбору ссылок закончена'


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [line.strip().split()[1] for line in file.readlines()]

    s = requests.Session()
    result_data = []
    urls_count = len(urls_list)
    for url in enumerate(urls_list):
        try:
            response = s.get(url=url[1], headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            game_title = soup.find('div').find('h1').text
            game_data_release = soup.find('div', class_='view').text.strip().replace('\n', '')
            game_img = f"https://gamebomb.ru{soup.find('div', class_='grid-100p-300-rc').find('div').find('img').get('src')}"
            game_info = soup.find('div', attrs={'id': 'article_content'}).text.strip().replace('\n', '')
            result_data.append(
                {
                    'original_url': url[1],
                    'game_title': game_title,
                    'game_data_release': game_data_release,
                    'game_img': game_img,
                    'game_info': game_info.strip()
                }
            )
            # print(game_title, game_info, game_data_release, game_img)
            print(f'Обработал {url[0] + 1}/{urls_count}')
        except Exception as ex:
            print(ex)

    with open('result.json', 'w', encoding='utf8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)

def main():
    # get_article_urls(url='https://gamebomb.ru/games')
    get_data('articles_description.txt')

if __name__ == '__main__':
    main()
