import json
from typing import Any

import pandas as pd

from src.logger import setup_logger

logger = setup_logger("utils")


def get_data_excel(file: str) -> Any:
    """Загружает данные из excel файла"""
    try:
        if file.endswith(".xls") or file.endswith(".xlsx"):
            df = pd.read_excel(file)

            logger.debug("Сформирован датафрейм с операциями")

            return df
        else:

            logger.error("Передан файл некорректного формата")

            raise ValueError("Файл некорректного формата")
    except FileNotFoundError:

        logger.error("Файл с операциями не найден")

        return "Файл с операциями не найден"


def make_listdict(data: pd.DataFrame) -> list:
    """Превращает датафрейм в список словарей"""
    transactions = data.to_dict(orient="records")

    logger.debug("Сформирован список словарей из датафрейма")

    return transactions


def get_settings(file: str) -> Any:
    """Получает пользовательские настройки из файла"""
    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)

            logger.debug("Загружены пользовательские настройки")

            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:

        logger.error(e)

        return "Файл с настройками не найден или некорректно закодирован"
