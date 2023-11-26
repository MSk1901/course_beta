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


def month_transactions(data: list[dict], date: str) -> list:
    """Возвращает транзакции только в текцщем месяце"""
    month = datetime.strptime(date, "%d.%m.%Y").strftime("%m.%Y")
    day = datetime.strptime(date, "%d.%m.%Y").day
    transactions = [x for x in data if month in str(x["Дата операции"]) and int(str(x["Дата операции"])[:2]) <= day]
    return transactions
