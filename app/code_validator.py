from settings import MAX_CHARS

# Функция, которая проверяет длину кода и возвращает (bool, сообщение об ошибке).
async def check_code_length(code: str, max_chars: int = MAX_CHARS) -> tuple:
    if len(code) > max_chars:
        return (False,
                f"❌ Код слишком длинный. Максимально допустимый размер: {max_chars} символов. "
                f"Ваш код содержит {len(code)} символов.")
    return True, ""