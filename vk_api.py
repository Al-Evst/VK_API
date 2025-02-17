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
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        response_data = response.json()

        if 'response' in response_data and 'short_url' in response_data['response']:
            return response_data['response']['short_url']

        raise ValueError("Ошибка: не удалось сократить ссылку.")
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except ValueError as e:
        print(str(e))
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
    
    return None  


def count_clicks(token, short_url, access_key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    
    try:
        parsed_url = urlparse(short_url)
        key = parsed_url.path.split('/')[1]

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

        if 'response' in response_json and 'views' in response_json['response']['stats'][0]:
            clicks_count = response_json['response']['stats'][0]['views']
            return clicks_count

        raise ValueError("Ошибка: не удалось получить количество кликов.")
    
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except ValueError as e:
        print(str(e))
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
    
    return None  


def is_shorten_link(token, url, access_key):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    
    try:
        parsed_url = urlparse(url)
        key = parsed_url.path.split('/')[1]

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
        
    except IndexError:
        return False
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
    
    return False 


def main():
    load_dotenv() 
    
    token = os.environ['VK_ACCESS_TOKEN']
    access_key = os.environ['ACCESS_KEY']

    if not token or not access_key:
        print("Ошибка: токен или access_key не найдены.")
        return

    url = input("Введите ссылку для сокращения: ")

    if is_shorten_link(token, url, access_key):
        clicks = count_clicks(token, url, access_key)
        if clicks is not None:
            print('Количество кликов: ', clicks)
    else:
        short_link = shorten_link(token, url)
        if short_link is not None:
            print('Сокращенная ссылка: ', short_link)


if __name__ == "__main__":
    main()
