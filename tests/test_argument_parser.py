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
    create_parser,
    parse_aggregate_condition,
    parse_arguments,
    parse_filter_condition,
)


class TestFilterOperator:
    """Тесты enum FilterOperator."""

    def test_operator_values(self):
        """Тестирует правильность значений операторов."""
        assert FilterOperator.EQUAL.value == "="
        assert FilterOperator.GREATER.value == ">"
        assert FilterOperator.LESS.value == "<"


class TestAggregateFunction:
    """Тесты enum AggregateFunction."""

    def test_function_values(self):
        """Тестирует правильность значений функций."""
        assert AggregateFunction.AVG.value == "avg"
        assert AggregateFunction.MIN.value == "min"
        assert AggregateFunction.MAX.value == "max"


class TestCreateParser:
    """Тесты создания парсера."""

    def test_create_parser_structure(self):
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


class TestParseFilterCondition:
    """Тесты парсинга условий фильтрации."""

    def test_parse_equal_condition(self):
        """Тестирует парсинг условия равенства."""
        condition = parse_filter_condition("price=100")

        assert condition.column == "price"
        assert condition.operator == FilterOperator.EQUAL
        assert condition.value == "100"

    def test_parse_greater_condition(self):
        """Тестирует парсинг условия больше."""
        condition = parse_filter_condition("quantity>50")

        assert condition.column == "quantity"
        assert condition.operator == FilterOperator.GREATER
        assert condition.value == "50"

    def test_parse_less_condition(self):
        """Тестирует парсинг условия меньше."""
        condition = parse_filter_condition("amount<1000")

        assert condition.column == "amount"
        assert condition.operator == FilterOperator.LESS
        assert condition.value == "1000"

    def test_parse_with_spaces(self):
        """Тестирует парсинг с пробелами."""
        condition = parse_filter_condition("  name = Apple  ")

        assert condition.column == "name"
        assert condition.operator == FilterOperator.EQUAL
        assert condition.value == "Apple"

    def test_parse_string_value(self):
        """Тестирует парсинг строковых значений."""
        condition = parse_filter_condition("category=Electronics")

        assert condition.column == "category"
        assert condition.operator == FilterOperator.EQUAL
        assert condition.value == "Electronics"

    def test_parse_value_with_spaces(self):
        """Тестирует парсинг значений с пробелами."""
        condition = parse_filter_condition("name=John Doe")

        assert condition.column == "name"
        assert condition.operator == FilterOperator.EQUAL
        assert condition.value == "John Doe"

    def test_parse_underscore_column(self):
        """Тестирует парсинг колонки с подчеркиванием."""
        condition = parse_filter_condition("user_id=123")

        assert condition.column == "user_id"
        assert condition.operator == FilterOperator.EQUAL
        assert condition.value == "123"

    def test_invalid_format_raises_error(self):
        """Тестирует что некорректный формат вызывает ошибку."""
        with pytest.raises(ValueError, match="Некорректный формат условия фильтрации"):
            parse_filter_condition("invalid")

        with pytest.raises(ValueError, match="Некорректный формат условия фильтрации"):
            parse_filter_condition("column")

        with pytest.raises(ValueError, match="Некорректный формат условия фильтрации"):
            parse_filter_condition("=value")

    def test_invalid_operator_raises_error(self):
        """Тестирует что неподдерживаемый оператор вызывает ошибку."""
        with pytest.raises(ValueError, match="Некорректный формат условия фильтрации"):
            parse_filter_condition("price!=100")

        with pytest.raises(ValueError, match="Некорректный формат условия фильтрации"):
            parse_filter_condition("amount>=50")

    def test_empty_string_raises_error(self):
        """Тестирует что пустая строка вызывает ошибку."""
        with pytest.raises(ValueError):
            parse_filter_condition("")

        with pytest.raises(ValueError):
            parse_filter_condition("   ")


class TestParseAggregateCondition:
    """Тесты парсинга условий агрегации."""

    def test_parse_avg_function(self):
        """Тестирует парсинг функции avg."""
        condition = parse_aggregate_condition("price=avg")

        assert condition.column == "price"
        assert condition.function == AggregateFunction.AVG

    def test_parse_min_function(self):
        """Тестирует парсинг функции min."""
        condition = parse_aggregate_condition("quantity=min")

        assert condition.column == "quantity"
        assert condition.function == AggregateFunction.MIN

    def test_parse_max_function(self):
        """Тестирует парсинг функции max."""
        condition = parse_aggregate_condition("amount=max")

        assert condition.column == "amount"
        assert condition.function == AggregateFunction.MAX

    def test_parse_with_spaces(self):
        """Тестирует парсинг с пробелами."""
        condition = parse_aggregate_condition("  price = avg  ")

        assert condition.column == "price"
        assert condition.function == AggregateFunction.AVG

    def test_parse_case_insensitive(self):
        """Тестирует парсинг функций в разном регистре."""
        condition1 = parse_aggregate_condition("price=AVG")
        condition2 = parse_aggregate_condition("price=Avg")
        condition3 = parse_aggregate_condition("price=aVg")

        assert condition1.function == AggregateFunction.AVG
        assert condition2.function == AggregateFunction.AVG
        assert condition3.function == AggregateFunction.AVG

    def test_underscore_column(self):
        """Тестирует парсинг колонки с подчеркиванием."""
        condition = parse_aggregate_condition("user_score=max")

        assert condition.column == "user_score"
        assert condition.function == AggregateFunction.MAX

    def test_invalid_format_raises_error(self):
        """Тестирует что некорректный формат вызывает ошибку."""
        with pytest.raises(ValueError, match="Некорректный формат условия агрегации"):
            parse_aggregate_condition("invalid")

        with pytest.raises(ValueError, match="Некорректный формат условия агрегации"):
            parse_aggregate_condition("column>avg")

        with pytest.raises(ValueError, match="Некорректный формат условия агрегации"):
            parse_aggregate_condition("=avg")

    def test_invalid_function_raises_error(self):
        """Тестирует что неподдерживаемая функция вызывает ошибку."""
        with pytest.raises(ValueError, match="Неподдерживаемая функция агрегации"):
            parse_aggregate_condition("price=sum")

        with pytest.raises(ValueError, match="Неподдерживаемая функция агрегации"):
            parse_aggregate_condition("price=count")

    def test_empty_string_raises_error(self):
        """Тестирует что пустая строка вызывает ошибку."""
        with pytest.raises(ValueError):
            parse_aggregate_condition("")

        with pytest.raises(ValueError):
            parse_aggregate_condition("   ")


class TestParseArguments:
    """Тесты основной функции парсинга аргументов."""

    def test_parse_filter_arguments(self):
        """Тестирует парсинг аргументов фильтрации."""
        args = parse_arguments(["data.csv", "--where", "price>100"])

        assert args.filename == "data.csv"
        assert args.filter_condition is not None
        assert args.filter_condition.column == "price"
        assert args.filter_condition.operator == FilterOperator.GREATER
        assert args.filter_condition.value == "100"
        assert args.aggregate_condition is None

    def test_parse_aggregate_arguments(self):
        """Тестирует парсинг аргументов агрегации."""
        args = parse_arguments(["sales.csv", "--aggregate", "revenue=avg"])

        assert args.filename == "sales.csv"
        assert args.aggregate_condition is not None
        assert args.aggregate_condition.column == "revenue"
        assert args.aggregate_condition.function == AggregateFunction.AVG
        assert args.filter_condition is None

    def test_complex_filename(self):
        """Тестирует сложные имена файлов."""
        args = parse_arguments(["/path/to/data-file_2023.csv", "--where", "id=1"])

        assert args.filename == "/path/to/data-file_2023.csv"
        assert args.filter_condition is not None

    def test_missing_filename_raises_error(self):
        """Тестирует что отсутствие имени файла вызывает ошибку."""
        with pytest.raises(SystemExit):  # argparse вызывает SystemExit
            parse_arguments(["--where", "price>100"])

    def test_missing_operation_raises_error(self):
        """Тестирует что отсутствие операции вызывает ошибку."""
        with pytest.raises(SystemExit):  # argparse вызывает SystemExit
            parse_arguments(["data.csv"])

    def test_both_operations_raises_error(self):
        """Тестирует что указание обеих операций вызывает ошибку."""
        with pytest.raises(SystemExit):  # mutually_exclusive_group
            parse_arguments(
                ["data.csv", "--where", "price>100", "--aggregate", "price=avg"]
            )

    def test_invalid_filter_condition_raises_error(self):
        """Тестирует что некорректное условие фильтрации вызывает ошибку."""
        with pytest.raises(ValueError):
            parse_arguments(["data.csv", "--where", "invalid_condition"])

    def test_invalid_aggregate_condition_raises_error(self):
        """Тестирует что некорректное условие агрегации вызывает ошибку."""
        with pytest.raises(ValueError):
            parse_arguments(["data.csv", "--aggregate", "invalid_condition"])


class TestNamedTuples:
    """Тесты для NamedTuple классов."""

    def test_filter_condition_creation(self):
        """Тестирует создание FilterCondition."""
        condition = FilterCondition("price", FilterOperator.GREATER, "100")

        assert condition.column == "price"
        assert condition.operator == FilterOperator.GREATER
        assert condition.value == "100"

    def test_aggregate_condition_creation(self):
        """Тестирует создание AggregateCondition."""
        condition = AggregateCondition("revenue", AggregateFunction.AVG)

        assert condition.column == "revenue"
        assert condition.function == AggregateFunction.AVG

    def test_arguments_creation(self):
        """Тестирует создание Arguments."""
        filter_cond = FilterCondition("price", FilterOperator.EQUAL, "100")
        args = Arguments("data.csv", filter_condition=filter_cond)

        assert args.filename == "data.csv"
        assert args.filter_condition == filter_cond
        assert args.aggregate_condition is None


class TestIntegration:
    """Интеграционные тесты."""

    def test_real_world_filter_scenarios(self):
        """Тестирует реальные сценарии фильтрации."""
        # Числовые условия
        args1 = parse_arguments(["products.csv", "--where", "price>500"])
        assert args1.filter_condition.value == "500"

        # Строковые условия
        args2 = parse_arguments(["users.csv", "--where", "name=John"])
        assert args2.filter_condition.value == "John"

        # Условия с пробелами в значении
        args3 = parse_arguments(["items.csv", "--where", "category=Home & Garden"])
        assert args3.filter_condition.value == "Home & Garden"

    def test_real_world_aggregate_scenarios(self):
        """Тестирует реальные сценарии агрегации."""
        # Среднее значение
        args1 = parse_arguments(["sales.csv", "--aggregate", "amount=avg"])
        assert args1.aggregate_condition.function == AggregateFunction.AVG

        # Минимум
        args2 = parse_arguments(["inventory.csv", "--aggregate", "stock=min"])
        assert args2.aggregate_condition.function == AggregateFunction.MIN

        # Максимум
        args3 = parse_arguments(["scores.csv", "--aggregate", "points=max"])
        assert args3.aggregate_condition.function == AggregateFunction.MAX
