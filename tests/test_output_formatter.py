import pytest
from src.output_formatter import OutputFormatter
from src.csv_reader import CSVReader
from tests.fixtures.csv_files import *

@pytest.mark.parametrize(
    "fixture_name,headers,expected_in_output",
    [
        ("simple_csv_file", ["name", "price"], ["Apple", "Banana", "100", "50"]),
        ("headers_csv_file", ["name", "price", "quantity"], ["Apple", "100", "5"]),
    ]
)
def test_display_table_output(capsys, request, fixture_name, headers, expected_in_output):
    """
    Проверяет, что display_table корректно выводит таблицу с помощью tabulate.
    """
    reader = CSVReader()
    file_path = request.getfixturevalue(fixture_name)
    _, csv_data = reader.read_file(str(file_path))
    formatter = OutputFormatter()
    formatter.display_table(csv_data, headers)
    captured = capsys.readouterr().out
    for item in expected_in_output:
        assert item in captured

@pytest.mark.parametrize(
    "column,function,result,expected",
    [
        ("price", "avg", 75.0, "AVG по столбцу 'price': 75"),
        ("quantity", "min", 5.0, "MIN по столбцу 'quantity': 5"),
        ("price", "max", 1234.5678, "MAX по столбцу 'price': 1235"),
        ("price", "avg", 12.3456, "AVG по столбцу 'price': 12.35"),
    ]
)
def test_display_aggregate_result(capsys, column, function, result, expected):
    """
    Проверяет, что display_aggregate_result корректно выводит результат агрегации.
    """
    formatter = OutputFormatter()
    formatter.display_aggregate_result(column, function, result)
    captured = capsys.readouterr().out
    assert expected in captured

def test_display_table_empty(capsys):
    formatter = OutputFormatter()
    formatter.display_table([], ["col1", "col2"])
    captured = capsys.readouterr().out
    assert "Нет данных для отображения." in captured

@pytest.mark.parametrize("value,expected", [
    (123.0, "123"),
    (123.456, "123.5"),
    (0.0001234, "0.0001234"),
    (100, "100"),
])
def test_format_number(value, expected):
    formatter = OutputFormatter()
    assert formatter._format_number(value) == expected 