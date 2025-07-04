"""
Модуль форматирования и вывода таблиц для CSV-обработчика.
"""
from typing import List, Dict, Union
from tabulate import tabulate

class OutputFormatter:
    """
    Класс для форматирования и вывода таблиц и результатов агрегации.
    """
    def display_table(self, data: List[Dict[str, str]], headers: List[str]) -> None:
        """
        Выводит таблицу данных в консоль с помощью tabulate.
        """
        if not data:
            print("Нет данных для отображения.")
            return
        table_data = self._prepare_table_data(data, headers)
        print(tabulate(table_data, headers=headers, tablefmt="grid", showindex=False))

    def display_aggregate_result(self, column: str, function: str, result: float) -> None:
        """
        Выводит результат агрегации в консоль.
        """
        formatted = self._format_number(result)
        print(f"{function.upper()} по столбцу '{column}': {formatted}")

    def _prepare_table_data(self, data: List[Dict[str, str]], headers: List[str]) -> List[List[str]]:
        """
        Подготовка данных для tabulate
        """
        return [[row.get(h, "") for h in headers] for row in data]

    def _format_number(self, value: Union[float, int]) -> str:
        """
        Форматирование числовых значений
        """
        if isinstance(value, float):
            return f"{value:.4g}" if value % 1 else f"{int(value)}"
        return str(value) 