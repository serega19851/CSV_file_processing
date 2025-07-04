"""
Модуль парсера аргументов командной строки для CSV обработчика.

Поддерживает парсинг команд фильтрации и агрегации:
- --where "column=value" | --where "column>value" | --where "column<value"
- --aggregate "column=function" (avg, min, max)
"""

import argparse
from enum import Enum
import re
from typing import NamedTuple, Optional


class FilterOperator(Enum):
    """Операторы фильтрации."""

    EQUAL = "="
    GREATER = ">"
    LESS = "<"


class AggregateFunction(Enum):
    """Функции агрегации."""

    AVG = "avg"
    MIN = "min"
    MAX = "max"


class SortDirection(Enum):
    """Направление сортировки."""

    ASC = "asc"
    DESC = "desc"


class FilterCondition(NamedTuple):
    """Условие фильтрации."""

    column: str
    operator: FilterOperator
    value: str


class AggregateCondition(NamedTuple):
    """Условие агрегации."""

    column: str
    function: AggregateFunction


class SortCondition(NamedTuple):
    """Условие сортировки."""

    column: str
    direction: SortDirection


class Arguments(NamedTuple):
    """Распарсенные аргументы командной строки."""

    filename: str
    filter_condition: Optional[FilterCondition] = None
    aggregate_condition: Optional[AggregateCondition] = None
    order_by_condition: Optional[SortCondition] = None


def create_parser() -> argparse.ArgumentParser:
    """
    Создает парсер аргументов командной строки.

    Returns:
        argparse.ArgumentParser: Настроенный парсер
    """
    parser = argparse.ArgumentParser(
        description="CSV файл обработчик с поддержкой фильтрации и агрегации",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python script.py data.csv --where "price>500"
  python script.py data.csv --where "name=Apple"
  python script.py data.csv --aggregate "price=avg"
  python script.py data.csv --aggregate "quantity=min"
        """,
    )

    parser.add_argument("filename", help="Путь к CSV файлу для обработки")

    group = parser.add_mutually_exclusive_group(required=False)

    group.add_argument(
        "--where",
        type=str,
        help='Условие фильтрации в формате "column=value", "column>value" или "column<value"',
    )

    group.add_argument(
        "--aggregate",
        type=str,
        help='Условие агрегации в формате "column=function" (avg, min, max)',
    )

    group.add_argument(
        "--order-by",
        type=str,
        help='Сортировка в формате "column=asc" или "column=desc"',
    )

    return parser


def parse_filter_condition(condition_str: str) -> FilterCondition:
    """
    Парсит строку условия фильтрации.

    Args:
        condition_str: Строка вида "column=value", "column>value" или "column<value"

    Returns:
        FilterCondition: Распарсенное условие

    Raises:
        ValueError: Если формат условия некорректен
    """
    # Регулярное выражение для парсинга условия (запрещает >= <= != и другие комбинации)
    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*(=|>|<)(?!=|>|<)\s*(.+)$"
    match = re.match(pattern, condition_str.strip())

    if not match:
        raise ValueError(
            f"Некорректный формат условия фильтрации: '{condition_str}'. "
            f"Ожидается формат 'column=value', 'column>value' или 'column<value'"
        )

    column, operator_str, value = match.groups()

    # Преобразуем оператор в enum
    try:
        operator = FilterOperator(operator_str)
    except ValueError:
        raise ValueError(
            f"Неподдерживаемый оператор: '{operator_str}'. " f"Поддерживаются: =, >, <"
        )

    return FilterCondition(
        column=column.strip(), operator=operator, value=value.strip()
    )


def parse_aggregate_condition(condition_str: str) -> AggregateCondition:
    """
    Парсит строку условия агрегации.

    Args:
        condition_str: Строка вида "column=function"

    Returns:
        AggregateCondition: Распарсенное условие

    Raises:
        ValueError: Если формат условия некорректен
    """
    # Регулярное выражение для парсинга условия агрегации
    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z]+)$"
    match = re.match(pattern, condition_str.strip())

    if not match:
        raise ValueError(
            f"Некорректный формат условия агрегации: '{condition_str}'. "
            f"Ожидается формат 'column=function'"
        )

    column, function_str = match.groups()

    # Преобразуем функцию в enum
    try:
        function = AggregateFunction(function_str.lower().strip())
    except ValueError:
        valid_functions = [f.value for f in AggregateFunction]
        raise ValueError(
            f"Неподдерживаемая функция агрегации: '{function_str}'. "
            f"Поддерживаются: {', '.join(valid_functions)}"
        )

    return AggregateCondition(column=column.strip(), function=function)


def parse_order_by_condition(condition_str: str) -> SortCondition:
    """Парсит строку условия сортировки."""
    pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(asc|desc)$"
    match = re.match(pattern, condition_str.strip(), flags=re.IGNORECASE)
    if not match:
        raise ValueError(
            f"Некорректный формат условия сортировки: '{condition_str}'. "
            f"Ожидается формат 'column=asc' или 'column=desc'"
        )

    column, direction_str = match.groups()
    direction = SortDirection(direction_str.lower())
    return SortCondition(column=column.strip(), direction=direction)


def parse_arguments(args: Optional[list[str]] = None) -> Arguments:
    """
    Парсит аргументы командной строки.

    Args:
        args: Список аргументов

    Returns:
        Arguments: Распарсенные и валидированные аргументы

    Raises:
        ValueError: Если аргументы некорректны
    """
    parser = create_parser()
    parsed = parser.parse_args(args)

    filter_condition = None
    aggregate_condition = None
    order_by_condition = None

    # Парсим условие фильтрации если есть
    if parsed.where:
        filter_condition = parse_filter_condition(parsed.where)

    # Парсим условие агрегации если есть
    if parsed.aggregate:
        aggregate_condition = parse_aggregate_condition(parsed.aggregate)

    # Парсим условие сортировки если есть
    if getattr(parsed, "order_by", None):
        order_by_condition = parse_order_by_condition(parsed.order_by)

    return Arguments(
        filename=parsed.filename,
        filter_condition=filter_condition,
        aggregate_condition=aggregate_condition,
        order_by_condition=order_by_condition,
    )
