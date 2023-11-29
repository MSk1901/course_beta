import os
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.logger import setup_logger

logger = setup_logger("reports")

PATH_TO_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "report.xlsx")


def report(*, filename: str = PATH_TO_FILE) -> Callable:
    """Записывает в файл результат, который возвращает функция, формирующая отчет"""
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Optional[Any], **kwargs: Optional[Any]) -> Optional[Any]:
            try:
                result = func(*args, **kwargs)
                if filename.endswith(".xlsx"):
                    result.to_excel(filename, index=False)

                    logger.debug(f"Данные записаны в файл {filename}")

                else:

                    logger.error("Некорректный формат файла")

                    raise ValueError("Файл некорректного формата")
            except Exception as e:

                logger.error(f"Возникла ошибка {e}")

                result = None
            return result
        return inner
    return wrapper


@report()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """Выводит траты по заданной категории за последние 3 месяца (от переданной даты)"""

    if not date:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y")

    start_date = end_date + relativedelta(months=-3)
    start_date_formatted = pd.to_datetime(start_date, dayfirst=True)
    end_date_formatted = pd.to_datetime(end_date, dayfirst=True)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    tr_by_dates = transactions[(transactions["Дата операции"] <= end_date_formatted) &
                               (transactions["Дата операции"] >= start_date_formatted)]
    spent_by_category = tr_by_dates[(tr_by_dates["Категория"] == category) & (tr_by_dates["Сумма операции"] < 0)]

    logger.debug("Сформирован датафрейм с операциями")

    return spent_by_category
