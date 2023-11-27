import os


from src.utils import get_data_excel, get_settings, make_listdict
from src.views import main_json
from src.services import search_phone_numbers
from src.reports import spending_by_category


FILE_TRANSACTIONS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xls")
FILE_SETTINGS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_settings.json")


def main():
    df = get_data_excel(FILE_TRANSACTIONS)
    transactions = make_listdict(df)
    settings = get_settings(FILE_SETTINGS)
    print(main_json(transactions, settings, "20.05.2020"))

    print(search_phone_numbers(transactions))

    spending_by_category(df, "Переводы", "20.05.2020")


if __name__ == '__main__':
    main()