"""
Тесты для модуля чтения CSV файлов.
"""

import pytest
from pathlib import Path
from src.csv_reader import CSVReader
from tests.fixtures.csv_files import (
    simple_csv_file,
    headers_csv_file,
    empty_csv_file,
    spaces_csv_file,
    only_headers_csv_file,
)

@pytest.mark.parametrize(
    "fixture_name,expected_headers,expected_data",
    [
        ("simple_csv_file", ["name", "price"], [
            {"name": "Apple", "price": "100"},
            {"name": "Banana", "price": "50"},
        ]),
        ("headers_csv_file", ["name", "price", "quantity"], [
            {"name": "Apple", "price": "100", "quantity": "5"},
        ]),
        ("spaces_csv_file", ["name", "description"], [
            {"name": "Apple", "description": "Red fruit"},
            {"name": "Banana", "description": "Yellow fruit"},
        ]),
        ("only_headers_csv_file", ["name", "price", "quantity"], []),
    ]
)
def test_read_file_parsing(request, fixture_name, expected_headers, expected_data):
    reader = CSVReader()
    file_path = request.getfixturevalue(fixture_name)
    headers, data = reader.read_file(str(file_path))
    assert headers == expected_headers
    assert data == expected_data

@pytest.mark.parametrize(
    "fixture_name,expected_exception,expected_message",
    [
        ("empty_csv_file", ValueError, "Файл пуст или не содержит заголовков"),
    ]
)
def test_read_file_errors(request, fixture_name, expected_exception, expected_message):
    reader = CSVReader()
    file_path = request.getfixturevalue(fixture_name)
    with pytest.raises(expected_exception, match=expected_message):
        reader.read_file(str(file_path))

def test_csv_reader_creation():
    reader = CSVReader()
    assert reader is not None

def test_read_file_handles_missing_file(tmp_path):
    reader = CSVReader()
    missing_file = tmp_path / "nonexistent_file.csv"
    with pytest.raises(FileNotFoundError, match="Файл не найден"):
        reader.read_file(str(missing_file))
