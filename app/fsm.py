from aiogram.fsm.state import State, StatesGroup

# Состояния для работы с ошибками
class ErrorStates(StatesGroup):
    waiting_for_error_codes = State()  # Ожидание кодов ошибок для добавления
    waiting_for_error_codes_to_delete = State()  # Ожидание кодов для удаления

# Состояния загрузки кода
class UploadFile(StatesGroup):
    waiting_for_upload_file = State() # Ожидание файла python
    waiting_for_upload_text = State() # Ожидание фрагмента кода python
