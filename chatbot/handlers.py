"""
Здесь находятся все хендлеры-валидаторы для сценариев бота.
Все хендлеры должны принимать только текст и контекст (словарь) и возвращать только флаг валидности
"""
import re


re_name = re.compile(r'^[\w\s-]{3,30}$')
re_email = re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Zа-яА-Я0-9-]+\.[a-zA-Zа-яА-Я0-9-.]+\b')


def handle_name(text, context):
    """
    Проверка валидности переданного имени.
    Если валидно, то записывает его в контекст и возвращает положительный флаг
    Parameters
    ----------
    text: str
        Сообщение, в котором должно быть только имя
    context: dict
        Словарь, в котором хранятся переменные состояния пользователя

    Returns
    -------
    bool
        Флаг валидности имени
    """
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    return False


def handle_email(text, context):
    """
    Ищет в сообщении и валидирует имейл.
    Если валидно, то записывает его в контекст и возвращает положительный флаг
    Parameters
    ----------
    text: str
        Сообщение с имейлом
    context: dict
        Словарь, в котором хранятся переменные состояния пользователя

    Returns
    -------
    bool
        Флаг валидности имейла
    """
    matches = re.findall(re_email, text)
    if matches:
        context['email'] = matches[0]
        return True
    return False
