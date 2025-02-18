import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, link):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': token,
        'v': '5.199',
        'url': link
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    response_data = response.json()

    if 'response' in response_data and 'short_url' in response_data['response']:
        return response_data['response']['short_url']
    else:
        raise ValueError("Ошибка: не удалось сократить ссылку.")


def count_clicks(token, short_url, access_key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'

    parsed_url = urlparse(short_url)
    path_parts = parsed_url.path.split('/')

    if len(path_parts) < 2:
        raise ValueError("Ошибка: недействительная сокращенная ссылка.")

    key = path_parts[1]

    params = {
        'access_token': token,
        'v': '5.199',
        'key': key,
        'access_key': access_key,
        'interval': 'forever'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    response_json = response.json()

    if 'response' in response_json and 'stats' in response_json['response'] and len(response_json['response']['stats']) > 0:
        clicks_count = response_json['response']['stats'][0]['views']
        return clicks_count
    else:
        raise ValueError("Ошибка: не удалось получить количество кликов.")


def is_shorten_link(token, url, access_key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')

    if len(path_parts) < 2:
        return False  

    key = path_parts[1]

    params = {
        'access_token': token,
        'v': '5.199',
        'key': key,
        'access_key': access_key,
        'interval': 'forever'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    response_json = response.json()

    return 'response' in response_json and 'stats' in response_json['response']


def main():
    load_dotenv()

    token = os.environ['VK_ACCESS_TOKEN']
    access_key = os.environ['ACCESS_KEY']

    if not (token and access_key):
        print("Ошибка: токен или access_key не найдены.")
        return

    url = input("Введите ссылку для сокращения: ")

    try:
        if is_shorten_link(token, url, access_key):
            clicks = count_clicks(token, url, access_key)  
            print(f'Количество кликов: {clicks}')
        else:
            short_link = shorten_link(token, url)  
            print(f'Сокращенная ссылка: {short_link}')

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except ValueError as e:
        print(f"Ошибка значения: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()
