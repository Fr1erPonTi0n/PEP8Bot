import asyncio
import logging

from aiogram import Bot, Dispatcher

from settings import TEL_TOKEN
from app.handlers import router
from services.random_image import get_random_imgur_image

bot = Bot(token=TEL_TOKEN)
dp = Dispatcher()

# Функция, которая обновляет список изображений каждую 1 минут.
async def update_images_periodically():
    from data.data import current_images  # Импортируем здесь, чтобы избежать циклического импорта
    while True:
        try:
            new_images = []
            # Получаем 5 новых изображения
            for _ in range(5):
                await asyncio.sleep(1)
                img = await get_random_imgur_image()
                if img:
                    new_images.append(img)
            if len(new_images) == 5:
                current_images[:] = new_images  # Изменяем список на месте
                print(f"Изображения были обновлены!")
            else:
                print('Изображения были не обновлены!')

        except Exception as e:
            print(f"Ошибка обновления изображения: {e}")

        await asyncio.sleep(440)


async def main():
    dp.include_router(router=router)

    # Создаем задачу для обновления изображений
    update_task = asyncio.create_task(update_images_periodically())

    try:
        await dp.start_polling(bot)
    finally:
        update_task.cancel()
        try:
            await update_task
        except asyncio.CancelledError:
            pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Выход из программы!')
