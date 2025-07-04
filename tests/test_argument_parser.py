"""
Тесты для модуля парсера аргументов командной строки.
"""

import pytest
from src.argument_parser import (
    AggregateCondition,
    AggregateFunction,
    Arguments,
    FilterCondition,
    FilterOperator,
    SortDirection,
    create_parser,
    parse_aggregate_condition,
    parse_arguments,
    parse_filter_condition,
    parse_order_by_condition,
)
from tests.fixtures.csv_files import (
    empty_csv_file,
    headers_csv_file,
    simple_csv_file,
)


def test_filter_operator_values():
    """Тестирует правильность значений операторов."""
    assert FilterOperator.EQUAL.value == "="
    assert FilterOperator.GREATER.value == ">"
    assert FilterOperator.LESS.value == "<"


def test_aggregate_function_values():
    """Тестирует правильность значений функций."""
    assert AggregateFunction.AVG.value == "avg"
    assert AggregateFunction.MIN.value == "min"
    assert AggregateFunction.MAX.value == "max"


def test_create_parser_structure():
    """Тестирует создание парсера с правильной структурой."""
    parser = create_parser()

    # Проверяем что парсер создался
    assert parser is not None
    assert parser.description is not None

    # Проверяем помощь
    help_text = parser.format_help()
    assert "filename" in help_text
    assert "--where" in help_text
    assert "--aggregate" in help_text


@pytest.mark.parametrize(
    "condition_str,expected_column,expected_operator,expected_value",
    [
        ("price=100", "price", FilterOperator.EQUAL, "100"),
        ("quantity>50", "quantity", FilterOperator.GREATER, "50"),
        ("amount<1000", "amount", FilterOperator.LESS, "1000"),
        ("  name = Apple  ", "name", FilterOperator.EQUAL, "Apple"),
        ("category=Electronics", "category", FilterOperator.EQUAL, "Electronics"),
        ("name=John Doe", "name", FilterOperator.EQUAL, "John Doe"),
        ("user_id=123", "user_id", FilterOperator.EQUAL, "123"),
    ],
)
def test_parse_filter_condition_valid(
    condition_str, expected_column, expected_operator, expected_value
):
    """Тестирует парсинг различных валидных условий фильтрации."""
    condition = parse_filter_condition(condition_str)

    assert condition.column == expected_column
    assert condition.operator == expected_operator
    assert condition.value == expected_value


@pytest.mark.parametrize(
    "invalid_condition,expected_error",
    [
        ("invalid", "Некорректный формат условия фильтрации"),
        ("column", "Некорректный формат условия фильтрации"),
        ("=value", "Некорректный формат условия фильтрации"),
        ("price!=100", "Некорректный формат условия фильтрации"),
        ("amount>=50", "Некорректный формат условия фильтрации"),
        ("", "Некорректный формат условия фильтрации"),
        ("   ", "Некорректный формат условия фильтрации"),
    ],
)
def test_parse_filter_condition_invalid(invalid_condition, expected_error):
    """Тестирует что некорректные условия фильтрации вызывают ошибку."""
    with pytest.raises(ValueError, match=expected_error):
        parse_filter_condition(invalid_condition)


@pytest.mark.parametrize(
    "condition_str,expected_column,expected_function",
    [
        ("price=avg", "price", AggregateFunction.AVG),
        ("quantity=min", "quantity", AggregateFunction.MIN),
        ("amount=max", "amount", AggregateFunction.MAX),
        ("  price = avg  ", "price", AggregateFunction.AVG),
        ("price=AVG", "price", AggregateFunction.AVG),
        ("price=Avg", "price", AggregateFunction.AVG),
        ("price=aVg", "price", AggregateFunction.AVG),
        ("user_score=max", "user_score", AggregateFunction.MAX),
    ],
)
def test_parse_aggregate_condition_valid(
    condition_str, expected_column, expected_function
):
    """Тестирует парсинг различных валидных условий агрегации."""
    condition = parse_aggregate_condition(condition_str)

    assert condition.column == expected_column
    assert condition.function == expected_function


@pytest.mark.parametrize(
    "invalid_condition,expected_error",
    [
        ("invalid", "Некорректный формат условия агрегации"),
        ("column>avg", "Некорректный формат условия агрегации"),
        ("price=sum", "Неподдерживаемая функция агрегации"),
        ("", "Некорректный формат условия агрегации"),
        ("   ", "Некорректный формат условия агрегации"),
    ],
)
def test_parse_aggregate_condition_invalid(invalid_condition, expected_error):
    """Тестирует что некорректные условия агрегации вызывают ошибку."""
    with pytest.raises(ValueError, match=expected_error):
        parse_aggregate_condition(invalid_condition)


@pytest.mark.parametrize(
    "csv_fixture_name,where_condition",
    [
        ("simple_csv_file", "price=100"),
        ("headers_csv_file", "quantity>0"),
        ("simple_csv_file", "name=Apple"),
    ],
)
def test_parse_arguments_filter(request, csv_fixture_name, where_condition):
    """Тестирует парсинг аргументов с фильтрацией."""
    csv_file = request.getfixturevalue(csv_fixture_name)
    args = parse_arguments([str(csv_file), "--where", where_condition])

    assert args.filename == str(csv_file)
    assert args.filter_condition is not None
    assert args.aggregate_condition is None


@pytest.mark.parametrize(
    "csv_fixture_name,aggregate_condition",
    [
        ("simple_csv_file", "price=avg"),
        ("headers_csv_file", "quantity=min"),
        ("simple_csv_file", "price=max"),
    ],
)
def test_parse_arguments_aggregate(request, csv_fixture_name, aggregate_condition):
    """Тестирует парсинг аргументов с агрегацией."""
    csv_file = request.getfixturevalue(csv_fixture_name)
    args = parse_arguments([str(csv_file), "--aggregate", aggregate_condition])

    assert args.filename == str(csv_file)
    assert args.filter_condition is None
    assert args.aggregate_condition is not None


def test_parse_arguments_complex_filename(tmp_path):
    """Тестирует сложные имена файлов."""
    complex_file = tmp_path / "complex file name.csv"
    complex_file.write_text("name,price\nApple,100")

    args = parse_arguments([str(complex_file), "--where", "price>50"])
    assert args.filename == str(complex_file)


@pytest.mark.parametrize(
    "invalid_args",
    [
        (["--where", "price>50"]),  # Нет файла
        (["test.csv"]),  # Нет операции
        (
            ["test.csv", "--where", "price>50", "--aggregate", "price=avg"]
        ),  # Обе операции
    ],
)
def test_parse_arguments_invalid(invalid_args):
    """Тестирует что некорректные аргументы вызывают ошибку."""
    with pytest.raises(SystemExit):
        parse_arguments(invalid_args)


def test_parse_arguments_invalid_filter_condition(simple_csv_file):
    """Тестирует что некорректное условие фильтрации вызывает ошибку."""
    with pytest.raises(ValueError):
        parse_arguments([str(simple_csv_file), "--where", "invalid"])


def test_parse_arguments_invalid_aggregate_condition(simple_csv_file):
    """Тестирует что некорректное условие агрегации вызывает ошибку."""
    with pytest.raises(ValueError):
        parse_arguments([str(simple_csv_file), "--aggregate", "invalid"])


def test_filter_condition_creation():
    """Тестирует создание FilterCondition."""
    condition = FilterCondition(
        column="price", operator=FilterOperator.GREATER, value="100"
    )

    assert condition.column == "price"
    assert condition.operator == FilterOperator.GREATER
    assert condition.value == "100"


def test_aggregate_condition_creation():
    """Тестирует создание AggregateCondition."""
    condition = AggregateCondition(column="price", function=AggregateFunction.AVG)

    assert condition.column == "price"
    assert condition.function == AggregateFunction.AVG


def test_arguments_creation():
    """Тестирует создание Arguments."""
    filter_condition = FilterCondition("price", FilterOperator.GREATER, "100")
    aggregate_condition = AggregateCondition("price", AggregateFunction.AVG)

    args = Arguments(
        filename="test.csv",
        filter_condition=filter_condition,
        aggregate_condition=aggregate_condition,
    )

    assert args.filename == "test.csv"
    assert args.filter_condition == filter_condition
    assert args.aggregate_condition == aggregate_condition


@pytest.mark.parametrize(
    "csv_fixture_name,filter_args,expected_column,expected_operator",
    [
        ("simple_csv_file", ["--where", "price>50"], "price", FilterOperator.GREATER),
        (
            "headers_csv_file",
            ["--where", "quantity=5"],
            "quantity",
            FilterOperator.EQUAL,
        ),
        ("simple_csv_file", ["--where", "name=Apple"], "name", FilterOperator.EQUAL),
    ],
)
def test_real_world_filter_scenarios(
    request, csv_fixture_name, filter_args, expected_column, expected_operator
):
    """Тестирует реальные сценарии фильтрации."""
    csv_file = request.getfixturevalue(csv_fixture_name)
    args = parse_arguments([str(csv_file)] + filter_args)

    assert args.filter_condition.column == expected_column
    assert args.filter_condition.operator == expected_operator


@pytest.mark.parametrize(
    "csv_fixture_name,aggregate_args,expected_column,expected_function",
    [
        (
            "simple_csv_file",
            ["--aggregate", "price=avg"],
            "price",
            AggregateFunction.AVG,
        ),
        (
            "headers_csv_file",
            ["--aggregate", "quantity=min"],
            "quantity",
            AggregateFunction.MIN,
        ),
        ("simple_csv_file", ["--aggregate", "price=max"], "price", AggregateFunction.MAX),
    ],
)
def test_real_world_aggregate_scenarios(
    request, csv_fixture_name, aggregate_args, expected_column, expected_function
):
    """Тестирует реальные сценарии агрегации."""
    csv_file = request.getfixturevalue(csv_fixture_name)
    args = parse_arguments([str(csv_file)] + aggregate_args)

    assert args.aggregate_condition.column == expected_column
    assert args.aggregate_condition.function == expected_function


@pytest.mark.parametrize("condition_str,expected_column,expected_direction", [
    ("price=asc", "price", SortDirection.ASC),
    ("brand=desc", "brand", SortDirection.DESC),
    ("  rating = desc  ", "rating", SortDirection.DESC),
])
def test_parse_order_by_condition_valid(condition_str, expected_column, expected_direction):
    condition = parse_order_by_condition(condition_str)
    assert condition.column == expected_column
    assert condition.direction == expected_direction


@pytest.mark.parametrize("invalid_condition", [
    "price", "price=>asc", "=asc", "price=down",
])
def test_parse_order_by_condition_invalid(invalid_condition):
    with pytest.raises(ValueError):
        parse_order_by_condition(invalid_condition)


@pytest.mark.parametrize("csv_fixture_name,order_arg,expected_column,expected_direction", [
    ("simple_csv_file", ["--order-by", "price=asc"], "price", SortDirection.ASC),
])
def test_parse_arguments_order_by(request, csv_fixture_name, order_arg, expected_column, expected_direction):
    csv_file = request.getfixturevalue(csv_fixture_name)
    args = parse_arguments([str(csv_file)] + order_arg)
    assert args.order_by_condition.column == expected_column
    assert args.order_by_condition.direction == expected_direction
    assert args.filter_condition is None
    assert args.aggregate_condition is None
