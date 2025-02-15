import requests
import re
import os
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('VK_ACCESS_TOKEN')
access_key = os.getenv('ACCESS_KEY')

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
        else:
            raise ValueError("Ошибка: не удалось сократить ссылку.")

    except requests.exceptions.HTTPError as e:
        return f"Ошибка HTTP: {e}"
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Произошла непредвиденная ошибка: {e}"

def count_clicks(token, short_url):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats' 
    params = {
        'access_token': token,
        'v': '5.199',
        'key': short_url.split('/')[3],
        'access_key' : access_key,
        'interval' : 'forever'
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        response_data = response.json()
        if 'response' in response_data and 'views' in response_data['response']['stats'][0]:
            clicks_count = response_data['response']['stats'][0]['views']
            return clicks_count
        else:
            raise ValueError("Ошибка: не удалось получить количество кликов.")

    except requests.exceptions.HTTPError as e:
        return f"Ошибка HTTP: {e}"
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Произошла непредвиденная ошибка: {e}"

def is_shorten_link(url):
    
    short_link_pattern = r'^https://vk\.cc/[a-zA-Z0-9]+$'
    if re.match(short_link_pattern, url):
        return True
    return False

def main():
    
    if not token or not access_key:
        print("Ошибка: токен или access_key не найдены.")
        return

    url = input("Введите ссылку для сокращения: ")

   
    if is_shorten_link(url):
        clicks = count_clicks(token, url)
        print('Количество кликов: ', clicks)
    else:
        shortened_url = shorten_link(token, url)
        print('Сокращенная ссылка: ', shortened_url)


if __name__ == "__main__":
    main()