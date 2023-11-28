import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(tr_list):
    df1 = pd.DataFrame(tr_list)
    result = spending_by_category(df1, "Супермаркеты").to_dict(orient="records")
    assert [x["Категория"] for x in result] == ["Супермаркеты", "Супермаркеты"]


def test_spending_by_category_with_date(tr_list):
    df1 = pd.DataFrame(tr_list)
    result = spending_by_category(df1, "Супермаркеты", "20.11.2023").to_dict(orient="records")
    assert [x["Категория"] for x in result] == ["Супермаркеты"]
