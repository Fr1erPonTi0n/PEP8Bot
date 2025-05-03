from settings import WHITE_LIST_CHATS, WHITE_LIST_USERS, WHITE_LIST_ENABLE

# Функция для проверки, находится ли чат в белом списке
async def is_chat_allowed(chat_id: int, user_id: int = None) -> bool | None:
    if not WHITE_LIST_ENABLE:
        return True
    if chat_id in WHITE_LIST_CHATS:
        return True
    if user_id and user_id in WHITE_LIST_USERS:
        return True
    return False