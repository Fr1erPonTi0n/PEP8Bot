from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать пользоваться ботом', callback_data='menu')],
])

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Загрузить код', callback_data='menu_upload_file')],
    [InlineKeyboardButton(text='Настройки', callback_data='settings'),
     InlineKeyboardButton(text='Помощь', callback_data='help')],
])

menus_upload_file = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Загрузить файл', callback_data='upload_file')],
    [InlineKeyboardButton(text='Вставить код как текст', callback_data='upload_text')],
    [InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
])

menu_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть ошибки', callback_data='see_errs')],
    [InlineKeyboardButton(text='Добавить исключение', callback_data='add_errs'),
     InlineKeyboardButton(text='Удалить исключение', callback_data='del_errs')],
    [InlineKeyboardButton(text='Вкл/выкл авто форматирование', callback_data='autoformat')],
    [InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
])

menu_autoformat = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
])

menu_help = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
])

menu_errors = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться назад', callback_data='cancel')]
])

menu_files = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться назад', callback_data='cancel')]
])