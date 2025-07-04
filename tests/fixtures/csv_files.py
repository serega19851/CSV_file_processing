import pytest


@pytest.fixture
def simple_csv_file(tmp_path):
    file_path = tmp_path / "test_simple.csv"
    file_path.write_text("name,price\nApple,100\nBanana,50")
    return file_path


@pytest.fixture
def headers_csv_file(tmp_path):
    file_path = tmp_path / "test_headers.csv"
    file_path.write_text("name,price,quantity\nApple,100,5")
    return file_path


@pytest.fixture
def empty_csv_file(tmp_path):
    file_path = tmp_path / "test_empty.csv"
    file_path.write_text("")
    return file_path


@pytest.fixture
def spaces_csv_file(tmp_path):
    file_path = tmp_path / "test_spaces.csv"
    file_path.write_text("name,description\nApple,Red fruit\nBanana,Yellow fruit")
    return file_path


@pytest.fixture
def only_headers_csv_file(tmp_path):
    file_path = tmp_path / "test_only_headers.csv"
    file_path.write_text("name,price,quantity")
    return file_path


@pytest.fixture
def csv_with_non_numeric(tmp_path):
    file_path = tmp_path / "test_csv_with_non_numeric.csv"
    file_path.write_text("name,price\nApple,100\nBanana,abc\nOrange,50")
    return file_path
