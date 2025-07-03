"""
Модуль для чтения и парсинга CSV файлов.
"""

import csv
from pathlib import Path
from typing import Dict, List, Tuple


class CSVReader:
    """
    Класс для чтения CSV файлов.
    """

    def read_file(self, filepath: str) -> Tuple[List[str], List[Dict[str, str]]]:
        """
        Читает CSV-файл и возвращает заголовки и данные.

        Args:
            filepath (str): Путь к CSV файлу.

        Returns:
            Tuple[List[str], List[Dict[str, str]]]:
                - headers: список заголовков
                - data: список строк в виде словарей

        Raises:
            FileNotFoundError: если файл не найден
            ValueError: если файл пуст или не содержит заголовков
        """
        # Проверка существования файла
        file = Path(filepath)
        if not file.exists():
            raise FileNotFoundError("Файл не найден")

        with file.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            if not headers:
                raise ValueError("Файл пуст или не содержит заголовков")
            data = [row for row in reader]
        return headers, data
