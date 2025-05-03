from pathlib import Path
from typing import List, Optional
import sqlite3

from data.data import valid_codes

# Определяем путь к базе данных
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "telegram.db"
VALID_CODES = valid_codes

# Функция, которая добавляет пользователя в БД
async def add_user(telegram_id: int, username: str = None) -> None:
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        result = cur.execute("SELECT * FROM users WHERE telegram_id = ?",
                             (telegram_id,)).fetchone()

        if not result:
            cur.execute("""INSERT INTO users (telegram_id, username) VALUES (?, ?)""",
                              (telegram_id, username))
            con.commit()

    except sqlite3.Error as e:
        print(f"Ошибка при извлечении данных: {e}")
    finally:
        con.close()

# Функция для фильтрации списка кодов ошибок, оставляя только валидные коды из errors_translation.json
async def filter_valid_error_codes(error_codes: List[str]) -> List[str]:
    return [code for code in error_codes if code in VALID_CODES]

# Функция для получения исключений ошибок по telegram_id
async def get_user_exceptions(telegram_id: int) -> List[str] or None:
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        results = cur.execute("""SELECT ue.error_code 
                                    FROM user_errors ue
                                    JOIN users u ON u.user_id = ue.user_id
                                    WHERE u.telegram_id = ?""", (telegram_id,)).fetchall()
        return [row[0] for row in results] if results else []
    except sqlite3.Error as e:
        print(f"Ошибка при извлечении данных: {e}")
        return []
    finally:
        con.close()

# Функция для включения или выключения авто форматирования кода
async def toggle_user_autoformat(telegram_id: int) -> tuple or None:
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        results = cur.execute("""SELECT autoformat
                                    FROM users
                                    WHERE telegram_id = ?""", (telegram_id,)).fetchone()

        if results is not None:
            autoformat_value = results[0]
            new_value = 0 if autoformat_value == 1 else 1  # Меняем значение на противоположное

            # Сохранить изменения
            cur.execute("""UPDATE users
                                SET autoformat = ?
                                WHERE telegram_id = ?""", (new_value, telegram_id))
            con.commit()

            return True, new_value, True  # (успешно изменено, новое значение, нет ошибки)

        return True, None, False  # Если пользователь не найден

    except sqlite3.Error as e:
        print(f"Ошибка при извлечении данных: {e}")
        return None, None, False  # (ошибка, нет значения)
    finally:
        con.close()

# Функция для получения состояния авто форматирования кода
async def is_user_autoformat_enabled(telegram_id: int) -> bool or None:
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        results = cur.execute("""SELECT autoformat
                                    FROM users
                                    WHERE telegram_id = ?""", (telegram_id,)).fetchone()

        if results is not None:
            return results[0] == 1

        return False

    except sqlite3.Error as e:
        print(f"Ошибка при извлечении данных: {e}")
        return False
    finally:
        con.close()

# Функция для добавления исключений ошибок по telegram_id
async def add_user_exceptions(telegram_id: int, error_codes: List[str]) -> bool or None:
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        # Получаем user_id
        user = cur.execute("SELECT user_id FROM users WHERE telegram_id = ?",
                           (telegram_id,)).fetchone()

        if not user:
            print(f"Пользователь {telegram_id} не найден!")
            return False

        user_id = user[0]

        error_codes = await filter_valid_error_codes(error_codes)

        # Добавляем все ошибки одним запросом
        cur.executemany(
            """INSERT OR IGNORE INTO user_errors (user_id, error_code) 
               VALUES (?, ?)""",
            [(user_id, code) for code in error_codes]
        )

        con.commit()
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных: {e}")
        return False
    finally:
        con.close()

# Функция для удаления исключений ошибок по telegram_id
async def del_user_exceptions(telegram_id: int, error_codes: Optional[List[str]] = None) -> bool or None:
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        user = cur.execute("SELECT user_id FROM users WHERE telegram_id = ?",
                           (telegram_id,)).fetchone()

        if not user:
            print(f"Пользователь {telegram_id} не найден!")
            return False

        user_id = user[0]

        if error_codes:
            cur.executemany(
                """DELETE FROM user_errors 
                   WHERE user_id = ? AND error_code = ?""",
                [(user_id, code) for code in error_codes]
            )
        else:
            cur.execute(
                """DELETE FROM user_errors 
                   WHERE user_id = ?""",
                (user_id,)
            )

        con.commit()
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при удалении данных: {e}")
        return False
    finally:
        con.close()