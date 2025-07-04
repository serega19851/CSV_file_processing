"""
Точка входа приложения CSV-обработчика
"""

import sys

from src.argument_parser import parse_arguments
from src.command_handler import CommandHandler


def main() -> int:
    """
    Главная функция приложения
    """
    try:
        args = parse_arguments()
        handler = CommandHandler()
        handler.execute(args)
        return 0
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
