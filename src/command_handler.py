"""
Координация выполнения команд
"""
from .argument_parser import Arguments, FilterCondition, AggregateCondition, SortCondition
from .csv_reader import CSVReader
from .filter_engine import filter_data
from .aggregator import Aggregator
from .output_formatter import OutputFormatter
# from operator import itemgetter

class CommandHandler:
    """
    Главный координатор выполнения команд
    """
    def __init__(self):
        self.csv_reader = CSVReader()
        self.aggregator = Aggregator()
        self.output_formatter = OutputFormatter()
        self.filter_engine = filter_data

    def execute(self, args: Arguments) -> None:
        """
        Выполнение команды на основе аргументов
        """
        try:
            if args.aggregate_condition:
                self._execute_aggregate(args.filename, args.aggregate_condition)
            elif args.filter_condition:
                self._execute_filter(args.filename, args.filter_condition)
            elif args.order_by_condition:
                self._execute_order_by(args.filename, args.order_by_condition)
            else:
                # Если не указано ни одного из аргументов — просто показать всю таблицу
                headers, data = self.csv_reader.read_file(args.filename)
                self.output_formatter.display_table(data, headers)
        except FileNotFoundError:
            print(f"Ошибка: файл '{args.filename}' не найден")
        except ValueError as e:
            print(f"Ошибка данных: {e}")
        except KeyError as e:
            print(f"Ошибка: столбец {e} не найден в данных")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

    def _execute_filter(self, file: str, condition: FilterCondition) -> None:
        """
        Выполнение фильтрации
        """
        headers, data = self.csv_reader.read_file(file)
        condition_str = f"{condition.column}{condition.operator.value}{condition.value}"
        filtered = self.filter_engine(data, condition_str)

        self.output_formatter.display_table(filtered, headers)

    def _execute_aggregate(self, file: str, condition: AggregateCondition) -> None:
        """
        Выполнение агрегации
        """
        _, data = self.csv_reader.read_file(file)
        condition_str = f"{condition.column}={condition.function.value}"
        result = self.aggregator.aggregate_data(data, condition_str)
        self.output_formatter.display_aggregate_result(condition.column, condition.function.value, result)

    def _execute_order_by(self, file: str, condition: SortCondition) -> None:
        """Выполнение сортировки"""
        headers, data = self.csv_reader.read_file(file)
        col = condition.column
        reverse = condition.direction == condition.direction.DESC

        def sort_key(row):
            value = row.get(col)
            try:
                return float(value)
            except (TypeError, ValueError):
                return value  # fallback to string

        sorted_data = sorted(data, key=sort_key, reverse=reverse)
        self.output_formatter.display_table(sorted_data, headers) 
