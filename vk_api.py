import requests
import re
import os
from dotenv import load_dotenv


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


def count_clicks(token, short_url,access_key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'v': '5.199',
        'key': short_url.split('/')[3],
        'access_key': access_key,
        'interval': 'forever'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    response_json = response.json()

    if 'response' in response_json and 'views' in response_json['response']['stats'][0]:
        clicks_count = response_json['response']['stats'][0]['views']
        return clicks_count
    else:
        raise ValueError("Ошибка: не удалось получить количество кликов.")


def is_shorten_link(token,url,access_key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    try:
        params = {
            'access_token': token,
            'v': '5.199',
            'key': url.split('/')[3],
            'access_key': access_key,
            'interval': 'forever'
        }

    

        response = requests.get(api_url, params=params)
        response.raise_for_status()
        response_json = response.json()

        if 'response' in response_json and 'stats' in response_json['response']:
            return True
        else:
            return False
        
    except IndexError:
        return False

def handle_exception(func):
    
    try:
        return func()
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except ValueError as e:
        print(str(e))
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


def main():

    load_dotenv() 
    
    token = os.environ['VK_ACCESS_TOKEN']
    access_key = os.environ['ACCESS_KEY']

    if not token or not access_key:
        print("Ошибка: токен или access_key не найдены.")
        return

    url = input("Введите ссылку для сокращения: ")

    if is_shorten_link(token,url,access_key):
        handle_exception(lambda: print('Количество кликов: ', count_clicks(token, url,access_key)))
    else:
        handle_exception(lambda: print('Сокращенная ссылка: ', shorten_link(token, url)))


if __name__ == "__main__":
    main()
