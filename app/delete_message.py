from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

# Функция, которая делает безопасное удаление сообщения (если возможно)
async def safe_delete_message(message: Message | CallbackQuery):
    try:
        if isinstance(message, CallbackQuery):
            await message.message.delete()
        else:
            await message.delete()
    except TelegramBadRequest:
        pass  # Сообщение уже удалено или недоступно
