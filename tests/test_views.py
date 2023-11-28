import json
from datetime import datetime
from unittest.mock import patch

import pytest
import requests

from src.views import (card_data, currency_rates, greeting, main_json, month_transactions, stock_rates,
                       top_five_transactions)


@pytest.mark.parametrize("data, expected_result", [
    (datetime(2023, 11, 27, 2, 15, 00, 65651), "Доброй ночи"),
    (datetime(2023, 11, 27, 8, 15, 00, 65651), "Доброе утро"),
    (datetime(2023, 11, 27, 15, 15, 00, 65651), "Добрый день"),
    (datetime(2023, 11, 27, 22, 15, 00, 65651), "Добрый вечер")])
@patch("src.views.datetime")
def test_greeting(mock_datetime, data, expected_result):
    mock_datetime.now.return_value = data
    assert greeting() == expected_result


def test_month_transactions(tr_list):
    assert [x['Дата операции'] for x in month_transactions(tr_list, "27.11.2023")] == ['27.11.2023 13:08:09',
                                                                                       '24.11.2023 18:57:06',
                                                                                       '17.11.2023 12:56:15',
                                                                                       '12.11.2023 11:50:27',
                                                                                       '05.11.2023 18:21:06']


def test_card_data(tr_list):
    dict_1 = {"last_digits": "1049", "total_spent": 1875.0, "cashback": 0}
    dict_2 = {"last_digits": "7842", "total_spent": 2490.99, "cashback": -394.0}
    dict_3 = {"last_digits": "9390", "total_spent": 577.0, "cashback": 24.0}

    result = card_data(tr_list, tr_list)

    assert dict_1 in result
    assert dict_2 in result
    assert dict_3 in result


def test_card_data_no_month_transactions(tr_list):
    dict_1 = {"last_digits": "1049", "total_spent": 0, "cashback": 0}
    dict_2 = {"last_digits": "7842", "total_spent": 0, "cashback": 0}
    dict_3 = {"last_digits": "9390", "total_spent": 0, "cashback": 0}

    result = card_data(tr_list, [])

    assert dict_1 in result
    assert dict_2 in result
    assert dict_3 in result


def test_top_five_transactions(tr_list):
    assert top_five_transactions(tr_list) == [{"date": "17.11.2023",
                                               "amount": -6200.0,
                                               "category": "Красота",
                                               "description": "ООО ЛАЗЕРСТАР_QR"},

                                              {"date": "27.11.2023",
                                               "amount": -1875.0,
                                               "category": "Переводы",
                                               "description": "Илья К."},

                                              {"date": "24.11.2023",
                                               "amount": -1176.99,
                                               "category": "Супермаркеты",
                                               "description": "Пятёрочка"},

                                              {"date": "06.09.2023",
                                               "amount": -900.0,
                                               "category": "Фастфуд",
                                               "description": "Port S N 8"},

                                              {"date": "05.11.2023",
                                               "amount": -465.0,
                                               "category": "Супермаркеты",
                                               "description": "WILDBERRIES"}
                                              ]


def test_top_five_transactions_no_transactions():
    assert top_five_transactions([]) == []


@patch.object(requests, 'get')
def test_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 100.0}}
    assert currency_rates(["USD"]) == [{"currency": "USD", "rate": 100.0}]


@pytest.mark.parametrize("error", [KeyError, ValueError, requests.exceptions.HTTPError])
@patch.object(requests, 'get')
def test_currency_rates_errors(mock_get, error):
    mock_get.side_effect = error
    with pytest.raises(ValueError):
        assert currency_rates(["mock"]) == "Что-то пошло не так"


@patch("src.views.os.getenv")
def test_currency_rates_no_api_key(mock_getenv):
    mock_getenv.return_value = None
    with pytest.raises(ValueError):
        assert currency_rates(["USD"]) == "Нет ключа API"


def test_currency_rates_no_currencies():
    assert currency_rates([]) == []


@patch.object(requests, 'get')
def test_stock_rates(mock_get):
    mock_get.return_value.json.return_value = {"c": 189.0}
    assert stock_rates(["AAPL"]) == [{"stock": "AAPL", "price": 189.0}]


@pytest.mark.parametrize("error", [KeyError, ValueError, requests.exceptions.HTTPError])
@patch.object(requests, 'get')
def test_stock_rates_errors(mock_get, error):
    mock_get.side_effect = error
    with pytest.raises(ValueError):
        assert stock_rates(["mock"]) == "Что-то пошло не так"


@patch("src.views.os.getenv")
def test_stock_rates_no_api_key(mock_getenv):
    mock_getenv.return_value = None
    with pytest.raises(ValueError):
        assert stock_rates(["AAPL"]) == "Нет ключа API"


def test_stock_rates_no_currencies():
    assert stock_rates([]) == []


@patch("src.views.stock_rates")
@patch("src.views.currency_rates")
@patch("src.views.card_data")
@patch("src.views.greeting")
def test_main_json(mock_greeting, mock_card_data, mock_currency_rates, mock_stock_rates, tr_list):
    mock_greeting.return_value = "Добрый вечер"
    mock_card_data.return_value = [
            {
                "last_digits": "1049",
                "total_spent": 1875.0,
                "cashback": 0
            },
            {
                "last_digits": "7842",
                "total_spent": 1176.99,
                "cashback": 11.0
            },
            {
                "last_digits": "9390",
                "total_spent": 465.0,
                "cashback": 23.0
            }
        ]
    mock_currency_rates.return_value = [{"currency": "USD", "rate": 100.0}]
    mock_stock_rates.return_value = [{"stock": "AAPL", "price": 189.0}]
    settings = {"user_currencies": ["USD"],
                "user_stocks": ["AAPL"]
                }
    result = json.loads(main_json(tr_list, settings, "27.11.2023"))
    assert result == {
        "greeting": "Добрый вечер",
        "cards": [
            {
                "last_digits": "1049",
                "total_spent": 1875.0,
                "cashback": 0
            },
            {
                "last_digits": "7842",
                "total_spent": 1176.99,
                "cashback": 11.0
            },
            {
                "last_digits": "9390",
                "total_spent": 465.0,
                "cashback": 23.0
            }
        ],
        "top_transactions": [
            {
                "date": "17.11.2023",
                "amount": -6200.0,
                "category": "Красота",
                "description": "ООО ЛАЗЕРСТАР_QR"
            },
            {
                "date": "27.11.2023",
                "amount": -1875.0,
                "category": "Переводы",
                "description": "Илья К."
            },
            {
                "date": "24.11.2023",
                "amount": -1176.99,
                "category": "Супермаркеты",
                "description": "Пятёрочка"
            },
            {
                "date": "05.11.2023",
                "amount": -465.0,
                "category": "Супермаркеты",
                "description": "WILDBERRIES"
            },
            {
                "date": "12.11.2023",
                "amount": -280.0,
                "category": "Мобильная связь",
                "description": "Мегафон +7 928 000-00-00"
            }
        ],
        "currency_rates": [
            {
                "currency": "USD",
                "rate": 100.0
            }
        ],
        "stock_prices": [
            {
                "stock": "AAPL",
                "price": 189.0
            }
        ]
    }
