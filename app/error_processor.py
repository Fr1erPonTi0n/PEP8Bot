import re
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from services.dbwork import add_user_exceptions, del_user_exceptions
import app.keyboards as kb

# Функция, которая обрабатывает коды ошибок для добавления/удаления.
async def process_error_codes(
        message: Message,
        state: FSMContext,
        action: str,
        success_message: str,
        error_message: str,
        all_flag: bool = False
) -> None:
    user_input = message.text.strip()
    telegram_id = message.from_user.id

    try:
        if all_flag and user_input.upper() == "ВСЁ":
            success = await del_user_exceptions(telegram_id)
            response = success_message if success else error_message
        else:
            error_codes = [code.strip() for code in re.split(r'[, ]+', user_input) if code.strip()]
            if not error_codes:
                await message.answer(
                    "❌ Не получены коды ошибок. Попробуйте еще раз.",
                    reply_markup=kb.menu_errors
                )
                return

            if action == "add":
                success = await add_user_exceptions(telegram_id, error_codes)
            else:
                success = await del_user_exceptions(telegram_id, error_codes)

            response = success_message if success else error_message

        await message.answer(
            response,
            reply_markup=kb.menu_settings
        )

    except Exception as e:
        print(str(e))
        await message.answer(
            f"❌ Ошибка при обработке запроса",
            reply_markup=kb.menu_errors
        )
    finally:
        await state.clear()