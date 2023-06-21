import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def get_headers(token):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }


def shorten_link(token, long_url):
    url = 'https://api-ssl.bitly.com/v4/shorten'

    data = {
        'long_url': long_url
    }

    headers = get_headers(token)

    response = requests.post(
        url=url,
        headers=headers,
        json=data,
        timeout=1)
        
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    url_parsed = urlparse(link)

    if url_parsed.netloc == 'bit.ly':
        url = f'https://api-ssl.bitly.com/v4/bitlinks/bit.ly{url_parsed.path}/clicks/summary'
        
        headers = get_headers(token)

        response = requests.get(
            url=url,
            headers=headers,
            timeout=1
        )

        response.raise_for_status()
        return response.json()['total_clicks']


def is_bitlink(url):
     return urlparse(url).netloc == 'bit.ly'


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('ACCESS_TOKEN')

    user_input = input('Введите ссылку: ')
    
    if is_bitlink(user_input):
        try:
            clicks_count = count_clicks(token=token, link=user_input)
        except requests.exceptions.HTTPError:
            exit('Введите правильный битлинк')
        print(f'По вашей ссылке прошли: {clicks_count} раз(а)')
    else:
        try:
            bitlink = shorten_link(token=token, long_url=user_input)
        except requests.exceptions.HTTPError:
            exit('Введите правильную ссылку')
        print(f'Ваш битлинк: {bitlink}')