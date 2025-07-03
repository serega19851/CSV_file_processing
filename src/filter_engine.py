"""
Модуль фильтрации данных для CSV.
"""

import re
from typing import Callable, Dict, List


def filter_data(rows: List[Dict[str, str]], condition: str) -> List[Dict[str, str]]:
    """
    Фильтрует строки по условию вида 'column_name=filter_value', 'column_name>filter_value', 'column_name<filter_value'.
    Поддерживаются операторы =, >, <.
    """
    match = re.match(r"^(\w+)([=<>])(.*)$", condition)
    if not match:
        raise ValueError("Некорректное условие фильтрации")
    column_name, operator_symbol, filter_value = match.groups()
    operator_map: Dict[str, Callable[[str, str], bool]] = {
        "=": lambda a, b: a == b,
        ">": lambda a, b: float(a) > float(b),
        "<": lambda a, b: float(a) < float(b),
    }
    if operator_symbol not in operator_map:
        raise ValueError(f"Оператор '{operator_symbol}' не поддерживается")

    compare = operator_map[operator_symbol]
    filtered_rows = []
    for row in rows:
        value = row.get(column_name)
        if value is None:
            continue
        try:
            if compare(value, filter_value):
                filtered_rows.append(row)
        except Exception:
            continue
    return filtered_rows
