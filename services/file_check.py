import subprocess
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
import asyncio
from typing import Optional, List, Dict
import os
from services.dbwork import get_user_exceptions

# Настраиваем пути
current_dir = Path(__file__).parent
translation_file = current_dir.parent / 'data' / 'errors_translation.json'

# Загрузка переводов ошибок
try:
    error_translations: Dict[str, str] = json.loads(translation_file.read_text(encoding='utf-8'))
except (FileNotFoundError, json.JSONDecodeError) as e:
    error_translations: Dict[str, str] = {}
    print(f"Ошибка загрузки файла переводов: {e}")

# Функция для проверки кода на соответствие PEP8.
async def check_pep8(source: str, telegram_id: Optional[int] = None) -> str or None:
    exceptions = await get_user_exceptions(telegram_id) if telegram_id else []

    try:
        # Создаем временный файл с явными правами доступа
        with NamedTemporaryFile(
                mode='w',
                suffix='.py',
                encoding='utf-8',
                delete=False
        ) as temp_file:
            temp_file.write(source)
            temp_file_path = temp_file.name

        # Запускаем проверку
        result = await asyncio.to_thread(_run_flake8, temp_file_path, exceptions)

        return result
    except Exception as e:
        print(f'Ошибка flask8: {e}')
        return "❌ Ошибка при проверки кода на соответствие PEP8"
    finally:
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except PermissionError:
                pass

# Функция для проверки файла на наличие ошибок pep8. Запускает flake8 для проверки файла.
def _run_flake8(file_path: str, exceptions: List[str]) -> str:
    try:
        result = subprocess.run(
            ['flake8', '--isolated', file_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
    except subprocess.SubprocessError as e:
        print(f"Ошибка при запуске проверки: {e}")
        return "❌ Ошибка при запуске проверки"

    if not result.stdout:
        return "✅ Код соответствует PEP8."

    output_lines = [">> Найдены ошибки PEP8 <<"]
    has_errors = False

    for line in result.stdout.splitlines():
        try:
            parts = line.split(":", 3)
            if len(parts) < 4:
                continue

            _, _, line_num, error = parts
            error_parts = error.strip().split()
            if not error_parts:
                continue

            col = error_parts[0].rstrip(':')
            error_code = error_parts[1] if len(error_parts) > 1 else ''

            if error_code in exceptions:
                continue

            has_errors = True
            original_error = ' '.join(error_parts[1:])
            error_msg = error_translations.get(error_code, original_error)
            error_details = f"{error_code}: {' '.join(error_parts[2:])}" if error_code else original_error

            output_lines.extend([
                f"\nСтрока: {line_num}, Символ: {col}",
                f"Ошибка: {error_msg} ( {error_details} )"
            ])
        except Exception as e:
            print(f"Ошибка обработки строки '{line}': {e}")
            continue

    return "\n".join(output_lines) if has_errors else "✅ Код соответствует PEP8."