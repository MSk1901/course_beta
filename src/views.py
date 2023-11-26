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
    else:
        greet = "Добрый вечер"
    return greet


def month_transactions(data: list[dict], date: str) -> list:
    """Возвращает транзакции только в текцщем месяце"""
    month = datetime.strptime(date, "%d.%m.%Y").strftime("%m.%Y")
    day = datetime.strptime(date, "%d.%m.%Y").day
    transactions = [x for x in data if month in str(x["Дата операции"]) and int(str(x["Дата операции"])[:2]) <= day]
    return transactions


def card_data(data: list[dict], data_month: list) -> list:
    """
    Формирует данные по каждой карте:
    - Последние 4 цифры карты
    - Общая сумма расходов
    - Кэшбэк
    """
    card_info = []
    cards = set([x["Номер карты"] for x in data if str(x["Номер карты"]) != "nan"])
    for card in cards:
        if data_month:
            card_transactions = [x for x in data_month if x["Номер карты"] == card]

            spending = -sum(x["Сумма операции"] for x in card_transactions if x["Сумма операции"] < 0)
            cashback = sum(x["Кэшбэк"] for x in card_transactions if x["Кэшбэк"] > 0 and str(x["Кэшбэк"] != "nan"))

            info = {"last_digits": card, "total_spent": spending, "cashback": cashback}
        else:
            info = {"last_digits": card, "total_spent": 0, "cashback": 0}
        card_info.append(info)
    return card_info


def top_five_transactions(data: list) -> list:
    """
    Выводит топ-5 операций по сумме платежа
    """
    if not data:
        return []
    else:
        transactions = []
        data_sorted = sorted(data, key=lambda x: abs(x["Сумма операции"]), reverse=True)
        top_five = data_sorted[:5]
        for tr in top_five:
            date = datetime.strptime(tr["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y")
            info = {"date": date,
                    "amount": tr["Сумма операции"],
                    "category": tr["Категория"],
                    "description": tr["Описание"]}
            transactions.append(info)
        return transactions
