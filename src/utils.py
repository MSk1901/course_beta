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
        return "Файл не найден"
