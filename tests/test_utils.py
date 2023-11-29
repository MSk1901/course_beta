from unittest.mock import patch

import pytest

from src.utils import get_data_excel, get_settings, make_listdict


@patch("src.utils.pd.read_excel")
def test_get_data_excel_valid_file(mock_read_excel, dataframe):
    mock_read_excel.return_value = dataframe
    result = get_data_excel("mock.xls")
    assert result.equals(dataframe)


@patch("src.utils.pd.read_excel")
def test_get_data_excel_invalid_file(mock_read_excel, dataframe):
    mock_read_excel.return_value = dataframe
    with pytest.raises(ValueError):
        assert get_data_excel("mock.csv") == "Файл некорректного формата"


def test_get_data_excel_file_notfound():
    assert get_data_excel("mock.xls") == "Файл с операциями не найден"


def test_make_listdict(dataframe):
    assert make_listdict(dataframe) == [{"date": "2023-09-05T11:30:32Z",
                                         "amount": "26165.0",
                                         "currency_name": "rubles",
                                         "currency_code": "RUB",
                                         },
                                        ]


@patch("src.utils.open")
def test_get_settings(mock_file):
    mock_file.return_value.__enter__.return_value.read.return_value = '[{"id": 1, "amount": 8563.45}]'
    assert get_settings("mock.json") == [{"id": 1, "amount": 8563.45}]


@patch("src.utils.open")
def test_get_settings_invalid_json(mock_file):
    mock_file.return_value.__enter__.return_value.read.return_value = '["id": 1, "amount": 8563.45}]'
    assert get_settings("mock.json") == "Файл с настройками не найден или некорректно закодирован"


def test_get_settings_no_file():
    assert get_settings("mock.json") == "Файл с настройками не найден или некорректно закодирован"
