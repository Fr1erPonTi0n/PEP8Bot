# PEP8Bot
Это телеграмм-бот для проверки кода Python на соответствие PEP 8.
Бот поможет преподавателям проверять код студентов на соответствие стандарту PEP 8. Он анализирует код с помощью flake8 и выводит понятные сообщения об ошибках с переводом на русский язык. Также бот может сделать автоформатирование всего кода - автоматическое исправление некоторых ошибок PEP 8 и результат отправить в виде отдельного сообщения с помощью библиотек autopep8 и black.

<div align="center">
  <br>
  <img src="https://i.imgur.com/b6VDIQZ.jpeg" alt="Прикольная фотография" width="400">
  <br>
</div>


# Функционал бота

Принимает код Python от пользователя через:

- Непосредственный ввод в чат (для небольших фрагментов)
- Загрузку .py файлов

Команды бота:

- **`/start`** - приветственное сообщение и краткая инструкция
- **`/menu`** - основное меню для работы с ботом
- **`/help`** - подробная справка по использованию бота
- **`/settings`** - настройки проверки (если потребуется)

# Структура бота

```
PEP8Bot/
├── app/
│   ├── code_processor.py       # Основная обработка кода
│   ├── code_validator.py       # Валидация кода по количеству символов
│   ├── delete_message.py       # Управление удалением сообщений
│   ├── error_processor.py      # Обработка исключений в виде ошибок  
│   ├── fsm.py                  # Конечные автоматы (Finite State Machine)
│   ├── handlers.py             # Основные обработчики команд бота
│   ├── keyboards.py            # Генерация клавиатур
│   ├── rate_limiter.py         # Лимитер запросов
│   └── whitelistcheck.py       # Проверка доступа по белому списку
│
├── data/
│   ├── data.py                 # Модуль работы с данными (переменными)
│   ├── errors_translation.json # Переводы ошибок PEP8
│   └── telegram.db             # База данных пользователей бота SQLite
│
├── services/
│   ├── autoformat.py           # Автоформатирование кода
│   ├── dbwork.py               # Работа с базой данных
│   ├── file_check.py           # Проверка PEP8
│   └── random_image.py         # Генерация изображений для бота
│
├── .gitignore                  # Список игнорируемых Git файлов
├── config.env                  # Конфигурационные переменные
├── main.py                     # Точка входа в приложение
├── README.md                   # Документация проекта
├── requirements.txt            # Зависимости Python
└── settings.py                 # Основные настройки приложения
```

# Как запустить бота?

Чтобы развернуть и запустить бота, выполните следующие шаги:  

#### **1. Клонируйте репозиторий**  
```bash
git clone https://github.com/Fr1erPonTi0n/PEP8Bot.git
cd PEP8Bot
```  

#### **2. Установите зависимости**  
```bash
pip install -r requirements.txt
```  

#### **3. Настройка конфигурации**  
Для начала конфигурации вы должны получить следующие API ключи:
- **Telegram Bot Token** – получите у [@BotFather](https://core.telegram.org/)  
- **Imgur API Client ID** – зарегистрируйте приложение на [Imgur API](https://apidocs.imgur.com/)

Дальше идут способы как настроить файлы конфигурации.

**Способ 1: Через терминал**

Выполните команду в терминале, указав ваш Telegram Bot Token и Imgur Client ID через пробел (без кавычек):

```bash
python create_config.py "ваш_токен-телеграмма" "ваш-imgur-client-id"
```

Дополнительно можно добавить пользователей и чаты в белый список при создании конфигурации. Укажите их ID через запятую:

```bash
python create_config.py "ваш_токен-телеграмма" "ваш-imgur-client-id" --chats 123,456 --users 789,012
```

Где:
- 123,456 - ID чатов через запятую
- 789,012 - ID пользователей через запятую

Если вы хотите настроить белый список, то вы должны поставить параметр **`WHITE_LIST_ENABLE=True`** в файле **`settings.py`**

**Способ 2: Ручное редактирование файла**

Откройте файл **`config.env`** и вручную добавьте API-ключи, а также списки пользователей и чатов (при необходимости). Пример заполнения:

```ini
# Telegram Bot
BOT_TOKEN=ваш-api-токен-телеграмма

# Imgur API
API_TOKEN=ваш-imgur-client-id  

# WhiteList Telegram
WHITE_LIST_CHATS=
WHITE_LIST_USERS=
```

Если вы хотите настроить белый список, то вы должны поставить параметр **`WHITE_LIST_ENABLE=True`** в файле **`settings.py`**

#### **4. Запуск бота**  
```bash
python main.py
```  

#### **Дополнительно**  
- Для изменения лимитов обработки измените **`MAX_CHARS`**, **`MAX_REQUESTS`** и **`ROLLBACK_TIME`** в **`settings.py`**
- Команда для быстрого запуска бота:

  На Linux:
  
  ```bash
  sudo apt-get update && sudo apt-get install -y git python3 python3-pip python3-venv && git clone https://github.com/Fr1erPonTi0n/PEP8Bot.git && cd PEP8Bot && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 create_config.py "ваш_telegram_bot_token" "ваш_imgur_api_token" && python3 main.py
  ```

  На Windows (если уже установлены [git](https://git-scm.com/downloads/) и [python](https://www.python.org/downloads/)):
  
  ```powershell
  git clone https://github.com/Fr1erPonTi0n/PEP8Bot.git && cd PEP8Bot && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python create_config.py "ваш_telegram_bot_token" "ваш_imgur_api_token" && python main.py
  ```

После запуска бот будет готов к работе! 🚀


