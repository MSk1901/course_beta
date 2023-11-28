import json

from src.services import search_phone_numbers


def test_search_phone_numbers(tr_list):
    result = json.loads(search_phone_numbers(tr_list))
    assert result == [{'date': '12.11.2023',
                       'amount': -280.0,
                       'category': 'Мобильная связь',
                       'description': 'Мегафон +7 928 000-00-00'}]


def test_search_phone_numbers_no_data():
    assert search_phone_numbers([]) == "[]"
