import subprocess
from tempfile import NamedTemporaryFile
import os
from typing import Tuple

# Функция, которая форматирует Python-код с помощью black и autopep8.
async def format_python_code(code: str, telegram_id: int = None) -> Tuple[bool, str]:
    try:
        # Создаем временный файл с автоматическим удалением
        with NamedTemporaryFile(
                mode='w+',
                suffix='.py',
                prefix=f'temp_code_{telegram_id}_' if telegram_id else 'temp_code_',
                encoding='utf-8',
                delete=False
        ) as tmp_file:
            tmp_file.write(code)
            tmp_path = tmp_file.name

        # Форматируем последовательно black и autopep8
        format_commands = [
            (['black', '--quiet', '--line-length', '88', tmp_path], "black"),
            (['autopep8', '--in-place', '--aggressive', tmp_path], "autopep8")
        ]

        for cmd, tool in format_commands:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"Ошибка {tool}: {result.stderr or 'неизвестная ошибка'}")
                return False, f"❌ Ошибка форматирования"

        # Читаем результат
        with open(tmp_path, 'r', encoding='utf-8') as f:
            return True, f.read()

    except subprocess.CalledProcessError as e:
        print(f"Ошибка {e}")
        return False, f"❌ Ошибка форматирования"
    except Exception as e:
        print(f"Ошибка {e}")
        return False, f"❌ Ошибка форматирования"
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass