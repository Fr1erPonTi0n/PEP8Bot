import time
from settings import MAX_REQUESTS, ROLLBACK_TIME

# Хранилище для отслеживания запросов пользователей
user_requests = {}

# Функция, которая проверяет, не превысил ли пользователь лимит запросов.
def check_rate_limit(user_id: int) -> bool:
    current_time = time.time()

    if user_id not in user_requests:
        user_requests[user_id] = {'count': 1, 'timestamp': current_time}
        return True

    user_data = user_requests[user_id]

    # Если прошло больше ROLLBACK_TIME секунд, сбрасываем счетчик
    if current_time - user_data['timestamp'] > ROLLBACK_TIME:
        user_data['count'] = 1
        user_data['timestamp'] = current_time
        return True

    # Если лимит запросов исчерпан
    if user_data['count'] >= MAX_REQUESTS:
        return False

    user_data['count'] += 1
    return True

# Функция, которая возвращает оставшееся время ожидания для пользователя.
def get_wait_time(user_id: int) -> int:
    if user_id not in user_requests:
        return 0
    return int(ROLLBACK_TIME - (time.time() - user_requests[user_id]['timestamp']))