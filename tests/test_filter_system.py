import pytest
from src.csv_reader import CSVReader
from src.filter_engine import filter_data
from tests.fixtures.csv_files import *


@pytest.mark.parametrize(
    "fixture_name,condition,expected_result",
    [
        ("simple_csv_file", "price=100", [{"name": "Apple", "price": "100"}]),
        ("simple_csv_file", "name=Banana", [{"name": "Banana", "price": "50"}]),
        ("simple_csv_file", "price>50", [{"name": "Apple", "price": "100"}]),
        ("simple_csv_file", "price<100", [{"name": "Banana", "price": "50"}]),
        (
            "headers_csv_file",
            "quantity=5",
            [{"name": "Apple", "price": "100", "quantity": "5"}],
        ),
        (
            "headers_csv_file",
            "price>50",
            [{"name": "Apple", "price": "100", "quantity": "5"}],
        ),
        (
            "headers_csv_file",
            "price<200",
            [{"name": "Apple", "price": "100", "quantity": "5"}],
        ),
        ("only_headers_csv_file", "price=100", []),
    ],
)
def test_filter_data_parametrized(request, fixture_name, condition, expected_result):
    """
    Проверяет, что функция filter_data корректно фильтрует строки по разным условиям:
    - Равенство, больше, меньше
    - Фильтрация по разным столбцам
    - Корректная работа при отсутствии подходящих строк
    """
    reader = CSVReader()
    file_path = request.getfixturevalue(fixture_name)
    _, csv_data = reader.read_file(str(file_path))
    filtered_result = filter_data(csv_data, condition)
    assert filtered_result == expected_result


@pytest.mark.parametrize(
    "test_rows,filter_condition,expected_exception_type,expected_exception_message",
    [
        (
            [{"a": "1"}],
            "b=1",
            None,
            None,
        ),
        ([{"a": "1"}], "a!1", ValueError, "Некорректное условие фильтрации"),
        (
            [{"a": "1"}],
            "a>abc",
            None,
            None,
        ),
    ],
)
def test_filter_data_errors(test_rows, filter_condition, expected_exception_type, expected_exception_message):
    """
    Проверяет обработку ошибок и граничных случаев:
    - Если столбца нет — возвращается пустой список
    - Если условие некорректно — выбрасывается ValueError
    - Если сравнение невозможно — возвращается пустой список
    """
    if expected_exception_type:
        with pytest.raises(expected_exception_type, match=expected_exception_message):
            filter_data(test_rows, filter_condition)
    else:
        assert filter_data(test_rows, filter_condition) == []


def test_filter_data_empty():
    """
    Проверяет, что функция возвращает пустой список, если входные данные пусты.
    """
    assert filter_data([], "a=1") == []
