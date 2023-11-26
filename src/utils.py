import json
from typing import Any

import pandas as pd


def get_data_excel(file: str) -> Any:
    """Загружает данные из excel файла"""
    try:
        if file.endswith(".xls") or file.endswith(".xlsx"):
            df = pd.read_excel(file)
            transactions = df.to_dict(orient="records")
            return transactions
        else:
            raise ValueError("Файл некорректного формата")
    except FileNotFoundError:
        return "Файл с операциями не найден"


def get_settings(file: str) -> Any:
    """Получает пользовательские настройки из файла"""
    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return "Файл с настройками не найден"
