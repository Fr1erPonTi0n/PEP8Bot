import requests
import random

from settings import CLIENT_ID_IMGUR

CLIENT_ID = CLIENT_ID_IMGUR

# Функция, которая получает случайные изображения с Imgur и возвращает его URL
async def get_random_imgur_image():
    headers = {'Authorization': f'Client-ID {CLIENT_ID}'}
    api_url = 'https://api.imgur.com/3/gallery/random/random/'

    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()  # Проверка на HTTP-ошибки

        data = response.json()
        images = data.get('data', [])

        if not images:
            return False

        # Фильтруем только изображения (исключаем альбомы и GIF, если нужно)
        valid_images = [
            img for img in images
            if not img.get('is_album') and img.get('type', '').startswith('image/')
        ]

        if not valid_images:
            return False

        random_image = random.choice(valid_images)
        return random_image.get('link', False)

    except (requests.RequestException, ValueError, KeyError):
        return False
