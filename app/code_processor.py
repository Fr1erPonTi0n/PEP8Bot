from typing import Optional
from aiogram.types import Message

from app.rate_limiter import check_rate_limit, get_wait_time
from app.code_validator import check_code_length
from services.autoformat import format_python_code
from services.dbwork import is_user_autoformat_enabled
from services.file_check import check_pep8

# Функция, которая обрабатывает Python код и возвращает результат или None если нужно отправить сообщение внутри функции
async def process_code(content: str, user_id: int, message: Message) -> Optional[tuple]:
    try:
        # Проверка лимита запросов
        if not check_rate_limit(user_id):
            wait_time = get_wait_time(user_id)
            await message.answer(
                f"❌ Слишком много запросов. Пожалуйста, подождите {wait_time} секунд."
            )
            return None

        # Проверка длины кода
        is_valid, error_msg = await check_code_length(content)
        if not is_valid:
            await message.answer(error_msg)
            return None

        # Нормализуем содержимое
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        content = '\n'.join(line.rstrip() for line in content.split('\n'))
        content = content.rstrip('\n')

        # Проверяем PEP8
        result_message = (await check_pep8(content, telegram_id=user_id),)

        # Авто форматирование кода (если включён)
        if await is_user_autoformat_enabled(telegram_id=user_id):
            autoformat_result = await format_python_code(content, telegram_id=user_id)
            if autoformat_result[0]:  # Если форматирование успешно
                autoformat_message = autoformat_result[1]
                result_message += (f">> Исправленный код <<\n{autoformat_message}",)
        else:
            result_message += (None,)

        return result_message

    except Exception as e:
        print(str(e))
        await message.answer("Ошибка при обработке кода")
        return None