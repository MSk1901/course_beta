from datetime import datetime


def greeting() -> str:
    """Создает привествие в зависимости от времени суток"""
    time = datetime.now().strftime("%H")
    if 0 <= int(time) <= 6:
        greet = "Доброй ночи"
    elif 6 <= int(time) < 12:
        greet = "Доброе утро"
    elif 12 <= int(time) < 18:
        greet = "Добрый день"
    elif 18 <= int(time) <= 24:
        greet = "Добрый вечер"
    return greet
