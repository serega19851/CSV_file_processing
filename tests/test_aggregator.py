import pytest
from src.aggregator import Aggregator
from src.csv_reader import CSVReader
from tests.fixtures.csv_files import *


@pytest.mark.parametrize(
    "fixture_name,condition,expected_result",
    [
        ("simple_csv_file", "price=avg", 75.0),
        ("simple_csv_file", "price=min", 50.0),
        ("simple_csv_file", "price=max", 100.0),
        ("headers_csv_file", "price=avg", 100.0),
        ("headers_csv_file", "quantity=min", 5.0),
        ("headers_csv_file", "quantity=max", 5.0),
        ("csv_with_non_numeric", "price=avg", 75.0),
        ("csv_with_non_numeric", "price=min", 50.0),
        ("csv_with_non_numeric", "price=max", 100.0),
    ]
)
def test_aggregate_data_parametrized(request, fixture_name, condition, expected_result):
    """
    Проверяет, что метод aggregate_data корректно вычисляет агрегацию (avg, min, max)
    по заданному столбцу и условию (например, 'price=avg') для разных наборов данных.
    В том числе, если в столбце есть нечисловые значения, они игнорируются.
    """
    reader = CSVReader()
    file_path = request.getfixturevalue(fixture_name)
    _, csv_data = reader.read_file(str(file_path))
    aggregator = Aggregator()
    result = aggregator.aggregate_data(csv_data, condition)
    assert result == expected_result

@pytest.mark.parametrize(
    "fixture_name,condition,expected_exception,expected_message",
    [
        ("simple_csv_file", "not_a_column=avg", ValueError, "Нет числовых значений в столбце"),
        ("simple_csv_file", "price=sum", ValueError, "Неподдерживаемая функция агрегации"),
        ("only_headers_csv_file", "price=avg", ValueError, "Нет числовых значений в столбце"),
        ("simple_csv_file", "badformat", ValueError, "Некорректный формат условия агрегации"),
        ("csv_with_non_numeric", "price=avg", None, None),
    ]
)
def test_aggregate_data_errors(request, fixture_name, condition, expected_exception, expected_message):
    """
    Проверяет обработку ошибок и граничных случаев:
    - Если столбца нет — выбрасывается ValueError
    - Если функция агрегации не поддерживается — выбрасывается ValueError
    - Если нет числовых значений — выбрасывается ValueError
    - Если формат условия некорректен — выбрасывается ValueError
    - Если в столбце есть нечисловые значения, но есть хотя бы одно число — нечисловые игнорируются
    """
    reader = CSVReader()
    file_path = request.getfixturevalue(fixture_name)
    _, csv_data = reader.read_file(str(file_path))
    aggregator = Aggregator()
    if expected_exception:
        with pytest.raises(expected_exception, match=expected_message):
            aggregator.aggregate_data(csv_data, condition)
    else:
        result = aggregator.aggregate_data(csv_data, condition)
        assert result == 75.0 