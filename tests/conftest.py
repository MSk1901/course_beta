import pandas as pd
import pytest


@pytest.fixture()
def tr_list():
    return [{'Дата операции': '27.11.2023 13:08:09',
             'Номер карты': "*1049",
             'Статус': 'OK',
             'Сумма операции': -1875.0,
             'Кэшбэк': 0,
             'Категория': 'Переводы',
             'Описание': 'Илья К.'
             },
            {'Дата операции': '24.11.2023 18:57:06',
             'Номер карты': "*7842",
             'Статус': 'OK',
             'Сумма операции': -1176.99,
             'Кэшбэк': 11.0,
             'Категория': 'Супермаркеты',
             'Описание': 'Пятёрочка'
             },
            {'Дата операции': '04.11.2023 11:58:52',
             'Номер карты': "*9390",
             'Статус': 'FAILED',
             'Сумма операции': -112.0,
             'Кэшбэк': 1.0,
             'Категория': 'Такси',
             'Описание': 'Яндекс Такси'
             },
            {'Дата операции': '17.11.2023 12:56:15',
             'Номер карты': "nan",
             'Статус': 'OK',
             'Сумма операции': -6200.0,
             'Кэшбэк': 62.0,
             'Категория': 'Красота',
             'Описание': 'ООО ЛАЗЕРСТАР_QR'
             },
            {'Дата операции': '12.11.2023 11:50:27',
             'Номер карты': "nan",
             'Статус': 'OK',
             'Сумма операции': -280.0,
             'Кэшбэк': "nan",
             'Категория': 'Мобильная связь',
             'Описание': 'Мегафон +7 928 000-00-00'
             },
            {'Дата операции': '05.11.2023 18:21:06',
             'Номер карты': "*9390",
             'Статус': 'OK',
             'Сумма операции': -465.0,
             'Кэшбэк': 23.0,
             'Категория': 'Супермаркеты',
             'Описание': 'WILDBERRIES'
             },
            {'Дата операции': '06.09.2023 12:29:33',
             'Номер карты': "*7842",
             'Статус': 'OK',
             'Сумма операции': -900.0,
             'Кэшбэк': 9.0,
             'Категория': 'Фастфуд',
             'Описание': 'Port S N 8'
             },
            {'Дата операции': '15.09.2023 16:50:31',
             'Номер карты': "*7842",
             'Статус': 'OK',
             'Сумма операции': -414.0,
             'Кэшбэк': -414.0,
             'Категория': 'Аптеки',
             'Описание': 'Аптека'
             },
            ]


@pytest.fixture
def dataframe():
    return pd.DataFrame([{"date": "2023-09-05T11:30:32Z",
                          "amount": "26165.0",
                          "currency_name": "rubles",
                          "currency_code": "RUB",
                          },
                         ])


@pytest.fixture()
def settings():
    return {
        "user_currencies": ["USD"],
        "user_stocks": ["AAPL"]
    }
