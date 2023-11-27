import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from src.logger import setup_logger

logger = setup_logger("views")


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

    logger.debug(f"Создано приветствие '{greet}'")

    return greet


def month_transactions(data: list[dict], date: str) -> list:
    """Возвращает транзакции только в текущем месяце"""
    month = datetime.strptime(date, "%d.%m.%Y").strftime("%m.%Y")
    day = datetime.strptime(date, "%d.%m.%Y").day
    transactions = [x for x in data if month in str(x["Дата операции"]) and int(str(x["Дата операции"])[:2]) <= day]

    logger.debug(f"Создан список транзакций за {month}")

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

            info = {"last_digits": card[1:], "total_spent": spending, "cashback": cashback}
        else:
            info = {"last_digits": card, "total_spent": 0, "cashback": 0}

        card_info.append(info)

    logger.debug(f"Получены данные по картам: {cards}")

    return card_info


def top_five_transactions(data: list) -> list:
    """
    Выводит топ-5 операций по сумме платежа
    """
    if not data:

        logger.debug("Нет транзакций за месяц")

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

        logger.debug("Получены 5 операций с наибольшей суммой платежа")

        return transactions


def currency_rates(currencies: list) -> list:
    """
    Выводит курс валют, выбранных пользователем
    """
    if not currencies:

        logger.debug("Пользователь не выбрал валюты")

        return []
    else:
        rates_info = []
        load_dotenv()
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if api_key is None:
            raise ValueError("Нет ключа API")
        try:
            for currency in currencies:
                url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
                response = requests.get(url, headers={'apikey': api_key})
                response.raise_for_status()
                response_data = response.json()
                rate = response_data["rates"]["RUB"]
                info = {"currency": currency, "rate": round(rate, 2)}
                rates_info.append(info)

            logger.debug(f"Получен курс валют для: {currencies}")

            return rates_info
        except (requests.exceptions.HTTPError, ValueError, KeyError) as e:

            logger.error(f"Возникла ошибка {e}")

            raise ValueError("Что-то пошло не так")


def stock_rates(stocks: list) -> list:
    """Получает стоимость акций из списка пользователя"""
    if not stocks:

        logger.debug("Пользователь не выбрал акции")

        return []
    else:
        stocks_info = []
        load_dotenv()
        api_key = os.getenv("STOCKS_API_KEY")
        if api_key is None:

            logger.error("Нет ключа API")

            raise ValueError("Нет ключа API")
        try:
            for stock in stocks:
                url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api_key}"
                response = requests.get(url)
                response.raise_for_status()
                response_data = response.json()
                stock_price = response_data["c"]
                info = {"stock": stock,
                        "price": stock_price}
                stocks_info.append(info)

            logger.debug(f"Получен курс валют для: {stocks}")

            return stocks_info
        except (requests.exceptions.HTTPError, ValueError, KeyError) as e:

            logger.error(f"Возникла ошибка {e}")

            raise ValueError("Что-то пошло не так")


def main_json(transactions: list, settings: dict, date: str) -> str:
    greet = greeting()
    tr_monthly = month_transactions(transactions, date)
    card_info = card_data(transactions, tr_monthly)
    top_five = top_five_transactions(tr_monthly)
    rates = currency_rates(settings["user_currencies"])
    stocks = stock_rates(settings["user_stocks"])
    response = {"greeting": greet,
                "cards": card_info,
                "top_transactions": top_five,
                "currency_rates": rates,
                "stock_prices": stocks}
    response_json = json.dumps(response, ensure_ascii=False, indent=4)

    logger.debug("Сформирован json-ответ")

    return response_json
