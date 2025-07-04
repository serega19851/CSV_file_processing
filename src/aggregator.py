"""
Система агрегации данных
"""
from typing import List, Dict, NamedTuple
from enum import Enum
import re

class AggregateFunction(Enum):
    AVG = "avg"
    MIN = "min"
    MAX = "max"

class AggregateCondition(NamedTuple):
    column: str
    function: AggregateFunction

class Aggregator:
    """
    Движок агрегации данных
    """
    def aggregate_data(self, data: List[Dict[str, str]], condition: str) -> float:
        """
        Агрегация данных по условию (например, 'price=avg')
        """
        aggregate_condition = self._parse_condition(condition)
        values = self._extract_numeric_values(data, aggregate_condition.column)
        return self._apply_function(values, aggregate_condition.function)

    def _parse_condition(self, condition: str) -> AggregateCondition:
        """
        Парсинг условия агрегации (например, 'price=avg')
        """
        pattern = r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z]+)$"
        match = re.match(pattern, condition.strip())
        if not match:
            raise ValueError(f"Некорректный формат условия агрегации: '{condition}'. Ожидается формат 'column=func'")
        column, function_str = match.groups()
        try:
            function = AggregateFunction(function_str.lower())
        except ValueError:
            valid = ', '.join(f.value for f in AggregateFunction)
            raise ValueError(f"Неподдерживаемая функция агрегации: '{function_str}'. Поддерживаются: {valid}")
        return AggregateCondition(column=column.strip(), function=function)

    def _extract_numeric_values(self, data: List[Dict[str, str]], column: str) -> List[float]:
        """
        Извлечение числовых значений из колонки
        """
        values = []
        for row in data:
            value = row.get(column)
            if value is None:
                continue
            try:
                values.append(float(value))
            except Exception:
                continue
        if not values:
            raise ValueError(f"Нет числовых значений в столбце '{column}' для агрегации")
        return values

    def _apply_function(self, values: List[float], function: AggregateFunction) -> float:
        """
        Применение функции агрегации
        """
        if function == AggregateFunction.AVG:
            return self._calculate_avg(values)
        elif function == AggregateFunction.MIN:
            return self._calculate_min(values)
        elif function == AggregateFunction.MAX:
            return self._calculate_max(values)

    def _calculate_avg(self, values: List[float]) -> float:
        return sum(values) / len(values)

    def _calculate_min(self, values: List[float]) -> float:
        return min(values)

    def _calculate_max(self, values: List[float]) -> float:
        return max(values) 