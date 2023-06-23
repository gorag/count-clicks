import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(headers, long_url):
    url = 'https://api-ssl.bitly.com/v4/shorten'

    json_long_url = {
        'long_url': long_url
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=json_long_url,
        timeout=1)
        
    response.raise_for_status()
    return response.json()['link']


def count_clicks(headers, link):
    parsed_url = urlparse(link)
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks\
        /{parsed_url.netloc}{parsed_url.path}/clicks/summary'

    response = requests.get(
        url=api_url,
        headers=headers,
        timeout=1
    )

    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(headers, url):
    parsed_url = urlparse(url)
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks\
        /{parsed_url.netloc}{parsed_url.path}'

    response = requests.get(
        url=api_url,
        headers=headers,
        timeout=1
    )
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    
    token = os.getenv('BITLY_TOKEN')

    headers = {
        'Authorization': f'Bearer {token}',
    }

    user_input = input('Введите ссылку: ')
    
    if is_bitlink(headers=headers, url=user_input):
        try:
            clicks_count = count_clicks(headers=headers, link=user_input)
        except requests.exceptions.HTTPError:
            print('Введите правильный битлинк')
        else:
            print(f'По вашей ссылке прошли: {clicks_count} раз(а)')
    else:
        try:
            bitlink = shorten_link(headers=headers, long_url=user_input)
        except requests.exceptions.HTTPError:
            print('Введите правильную ссылку')
        else:
            print(f'Ваш битлинк: {bitlink}')
