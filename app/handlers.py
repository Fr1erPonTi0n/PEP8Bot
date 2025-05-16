from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.code_processor import process_code
from app.error_processor import process_error_codes
from app.whitelistcheck import is_chat_allowed
import app.keyboards as kb
from app.delete_message import safe_delete_message
from app.fsm import ErrorStates, UploadFile

from services.dbwork import get_user_exceptions, toggle_user_autoformat, add_user

from data.data import *

router = Router()


# -- Старт --


@router.message(CommandStart())
async def cmd_start(message: Message):
    if not await is_chat_allowed(message.chat.id, message.from_user.id):
        return

    await add_user(telegram_id=message.from_user.id, username=message.from_user.username)

    await message.answer_photo(
        photo=current_images[0],
        caption=start_message,
        reply_markup=kb.start
    )


# -- Меню --


@router.message(Command('menu'))
@router.callback_query(F.data == 'menu')
async def menu_handler(update: Message | CallbackQuery):
    if isinstance(update, Message):
        if not await is_chat_allowed(update.chat.id, update.from_user.id):
            return
        await safe_delete_message(update)
        await update.answer('Перемещение в главное меню')
        msg = update
    else:
        if not await is_chat_allowed(update.message.chat.id, update.from_user.id):
            return
        await safe_delete_message(update)
        await update.answer('Перемещение в главное меню')
        msg = update.message

    await msg.answer_photo(
        photo=current_images[1],
        caption=menu_message,
        reply_markup=kb.menu
    )


# -- Работа с файлами --


@router.callback_query(F.data == 'menu_upload_file')
async def menu_upload_file_handler(callback: CallbackQuery):
    if not await is_chat_allowed(callback.message.chat.id, callback.from_user.id):
        return

    await safe_delete_message(callback)
    await callback.answer('Начало работы с файлами')
    await callback.message.answer_photo(
        photo=current_images[4],
        caption=upload_file_message,
        reply_markup=kb.menus_upload_file
    )


@router.callback_query(F.data.in_(['upload_file', 'upload_text']))
async def upload_handler(callback: CallbackQuery, state: FSMContext):
    if not await is_chat_allowed(callback.message.chat.id, callback.from_user.id):
        return

    await safe_delete_message(callback)
    await callback.answer('Начало работы с файлами')

    if callback.data == 'upload_file':
        await state.set_state(UploadFile.waiting_for_upload_file)
        caption = upload_file_message_one
    else:
        await state.set_state(UploadFile.waiting_for_upload_text)
        caption = upload_file_message_two

    await callback.message.answer_photo(
        photo=current_images[3],
        caption=caption,
        reply_markup=kb.menu_files
    )


# -- Обработчик загрузки --


@router.message(UploadFile.waiting_for_upload_file)
async def process_upload_file(message: Message, state: FSMContext):
    if not message.document:
        await message.answer("Пожалуйста, отправьте файл с Python кодом.")
        return

    # Проверяем, что файл имеет расширение .py
    if not message.document.file_name.lower().endswith('.py'):
        await message.answer("❌ Файл должен иметь расширение .py!")
        return

    try:
        file_info = await message.bot.get_file(message.document.file_id)
        downloaded_file = await message.bot.download_file(file_info.file_path)
        content = downloaded_file.read().decode('utf-8')
        result = await process_code(content, message.from_user.id, message)
        await message.answer(result[0])
        if result[1] is not None:
            await message.answer(result[1])
    except Exception as e:
        print(str(e))
        await message.answer(f"Ошибка при обработке файла")
    finally:
        await state.clear()


@router.message(UploadFile.waiting_for_upload_text)
async def process_upload_text(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправьте текст Python кода.")
        return

    try:
        result = await process_code(message.text, message.from_user.id, message)
        await message.answer(result[0])
        if result[1] is not None:
            await message.answer(result[1])
    except Exception as e:
        print(str(e))
        await message.answer(f"Ошибка при обработке текста")
    finally:
        await state.clear()


# -- Помощь --


@router.message(Command('help'))
@router.callback_query(F.data == 'help')
async def help_handler(update: Message | CallbackQuery):
    if isinstance(update, Message):
        if not await is_chat_allowed(update.chat.id, update.from_user.id):
            return
        await safe_delete_message(update)
        msg = update
    else:
        if not await is_chat_allowed(update.message.chat.id, update.from_user.id):
            return
        await safe_delete_message(update)
        await update.answer('Вы выбрали помощь')
        msg = update.message

    await msg.answer_photo(
        photo=current_images[2],
        caption=help_message,
        reply_markup=kb.menu_help
    )


# -- Настройки --


@router.message(Command('settings'))
@router.callback_query(F.data == 'settings')
async def settings_handler(update: Message | CallbackQuery):
    if isinstance(update, Message):
        if not await is_chat_allowed(update.chat.id, update.from_user.id):
            return
        await safe_delete_message(update)
        msg = update
    else:
        if not await is_chat_allowed(update.message.chat.id, update.from_user.id):
            return
        await safe_delete_message(update)
        await update.answer('Вы выбрали настройки')
        msg = update.message

    await msg.answer_photo(
        photo=current_images[3],
        caption=setting_message,
        reply_markup=kb.menu_settings
    )


# -- Включение или выключение авто форматирования --


@router.callback_query(F.data == 'autoformat')
async def autoformat_true_or_false(callback: CallbackQuery):
    if not await is_chat_allowed(callback.message.chat.id, callback.from_user.id):
        return

    await safe_delete_message(callback)
    await callback.answer('')

    result = await toggle_user_autoformat(telegram_id=callback.from_user.id)
    if result[2]:  # Проверяем статус ошибки
        if result[1] == 1:  # Если автоформат включен
            await callback.message.answer_photo(
                photo=current_images[2],
                caption=on_autoformat,
                reply_markup=kb.menu_autoformat
            )
        else:  # Если автоформат выключен
            await callback.message.answer_photo(
                photo=current_images[3],
                caption=off_autoformat,
                reply_markup=kb.menu_autoformat
            )
    else:  # Если произошла ошибка
        await callback.message.answer_photo(
            photo=current_images[1],
            caption=error_autoformat,
            reply_markup=kb.menu_autoformat
        )


# -- Вывод существующих ошибок --


@router.callback_query(F.data == 'see_errs')
async def see_user_errors(callback: CallbackQuery):
    if not await is_chat_allowed(callback.message.chat.id, callback.from_user.id):
        return

    await safe_delete_message(callback)
    await callback.answer('Вы выбрали посмотреть ошибки')

    result = await get_user_exceptions(callback.from_user.id)
    caption = (
        f'Вот ваши исключения: {", ".join(result)}' if result
        else 'У вас нету исключений!'
    )

    await callback.message.answer_photo(
        photo=current_images[4],
        caption=caption,
        reply_markup=kb.menu_errors
    )


# -- Добавление ошибок --


@router.callback_query(F.data == 'add_errs')
async def add_user_errors(callback: CallbackQuery, state: FSMContext):
    if not await is_chat_allowed(callback.message.chat.id, callback.from_user.id):
        return

    await safe_delete_message(callback)
    await callback.answer('Вы выбрали добавление ошибок')
    await state.set_state(ErrorStates.waiting_for_error_codes)

    await callback.message.answer_photo(
        photo=current_images[2],
        caption=add_error_message,
        reply_markup=kb.menu_errors
    )


# -- Удаление ошибок --


@router.callback_query(F.data == 'del_errs')
async def del_user_errors(callback: CallbackQuery, state: FSMContext):
    if not await is_chat_allowed(callback.message.chat.id, callback.from_user.id):
        return

    await safe_delete_message(callback)
    await callback.answer('Вы выбрали удаление ошибок')
    await state.set_state(ErrorStates.waiting_for_error_codes_to_delete)

    await callback.message.answer_photo(
        photo=current_images[1],
        caption=delete_error_message,
        reply_markup=kb.menu_errors
    )


# -- Обработка состояний кодов --


@router.message(ErrorStates.waiting_for_error_codes)
async def process_error_codes_adding(message: Message, state: FSMContext):
    await process_error_codes(
        message=message,
        state=state,
        action="add",
        success_message="✅ Коды ошибок успешно добавлены, некорректные коды были удалены!",
        error_message="❌ Произошла ошибка при добавлении кодов. Попробуйте позже."
    )


@router.message(ErrorStates.waiting_for_error_codes_to_delete)
async def process_error_codes_deletion(message: Message, state: FSMContext):
    await process_error_codes(
        message=message,
        state=state,
        action="delete",
        success_message="✅ Коды ошибок успешно удалены!",
        error_message="❌ Произошла ошибка при удалении кодов",
        all_flag=True
    )


# -- Отмена действий --


@router.callback_query(F.data == 'cancel')
async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    if not await is_chat_allowed(callback.message.chat.id, callback.from_user.id):
        return

    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await callback.answer("Операция отменена")
    else:
        await callback.answer("Нет активных операций для отмены")

    await safe_delete_message(callback)
    await callback.message.answer_photo(
        photo=current_images[1],
        caption=menu_message,
        reply_markup=kb.menu
    )
