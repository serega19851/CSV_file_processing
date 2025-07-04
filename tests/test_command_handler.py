import pytest
from unittest.mock import Mock, patch, MagicMock
from src.command_handler import CommandHandler
from src.argument_parser import Arguments, FilterCondition, AggregateCondition, FilterOperator, AggregateFunction

def test_command_handler_initialization():
    """Тест инициализации CommandHandler"""
    handler = CommandHandler()
    assert handler.csv_reader is not None
    assert handler.aggregator is not None
    assert handler.output_formatter is not None

def test_execute_calls_simple_display():
    """Тест что execute вызывает простой вывод когда нет where и aggregate"""
    handler = CommandHandler()
    args = Arguments(filename="test.csv")
    
    with patch.object(handler.csv_reader, 'read_file') as mock_read:
        with patch.object(handler.output_formatter, 'display_table') as mock_display:
            mock_read.return_value = (["name", "price"], [{"name": "Apple", "price": "100"}])
            
            handler.execute(args)
            
            mock_read.assert_called_once_with("test.csv")
            mock_display.assert_called_once_with([{"name": "Apple", "price": "100"}], ["name", "price"])

def test_execute_calls_filter_when_where_provided():
    """Тест что execute вызывает _execute_filter когда указан where"""
    handler = CommandHandler()
    filter_condition = FilterCondition(column="price", operator=FilterOperator.GREATER, value="100")
    args = Arguments(filename="test.csv", filter_condition=filter_condition)
    
    with patch.object(handler, '_execute_filter') as mock_filter:
        handler.execute(args)
        mock_filter.assert_called_once_with("test.csv", filter_condition)

def test_execute_calls_aggregate_when_aggregate_provided():
    """Тест что execute вызывает _execute_aggregate когда указан aggregate"""
    handler = CommandHandler()
    aggregate_condition = AggregateCondition(column="price", function=AggregateFunction.AVG)
    args = Arguments(filename="test.csv", aggregate_condition=aggregate_condition)
    
    with patch.object(handler, '_execute_aggregate') as mock_aggregate:
        handler.execute(args)
        mock_aggregate.assert_called_once_with("test.csv", aggregate_condition)

def test_execute_prioritizes_aggregate_over_where():
    """Тест что execute приоритизирует aggregate над where"""
    handler = CommandHandler()
    filter_condition = FilterCondition(column="price", operator=FilterOperator.GREATER, value="100")
    aggregate_condition = AggregateCondition(column="price", function=AggregateFunction.AVG)
    args = Arguments(filename="test.csv", filter_condition=filter_condition, aggregate_condition=aggregate_condition)
    
    with patch.object(handler, '_execute_aggregate') as mock_aggregate:
        with patch.object(handler, '_execute_filter') as mock_filter:
            handler.execute(args)
            mock_aggregate.assert_called_once_with("test.csv", aggregate_condition)
            mock_filter.assert_not_called()

@patch('src.command_handler.filter_data')
def test_execute_filter_calls_correct_methods(mock_filter_data):
    """Тест что _execute_filter вызывает правильные методы"""
    handler = CommandHandler()
    filter_condition = FilterCondition(column="price", operator=FilterOperator.GREATER, value="50")
    
    with patch.object(handler.csv_reader, 'read_file') as mock_read:
        with patch.object(handler.output_formatter, 'display_table') as mock_display:
            mock_read.return_value = (["name", "price"], [{"name": "Apple", "price": "100"}])
            mock_filter_data.return_value = [{"name": "Apple", "price": "100"}]
            
            handler._execute_filter("test.csv", filter_condition)
            
            mock_read.assert_called_once_with("test.csv")
            mock_filter_data.assert_called_once_with([{"name": "Apple", "price": "100"}], "price>50")
            mock_display.assert_called_once_with([{"name": "Apple", "price": "100"}], ["name", "price"])

def test_execute_aggregate_calls_correct_methods():
    """Тест что _execute_aggregate вызывает правильные методы"""
    handler = CommandHandler()
    aggregate_condition = AggregateCondition(column="price", function=AggregateFunction.AVG)
    
    with patch.object(handler.csv_reader, 'read_file') as mock_read:
        with patch.object(handler.aggregator, 'aggregate_data') as mock_aggregate:
            with patch.object(handler.output_formatter, 'display_aggregate_result') as mock_display:
                mock_read.return_value = (["name", "price"], [{"name": "Apple", "price": "100"}])
                mock_aggregate.return_value = 75.0
                
                handler._execute_aggregate("test.csv", aggregate_condition)
                
                mock_read.assert_called_once_with("test.csv")
                mock_aggregate.assert_called_once_with([{"name": "Apple", "price": "100"}], "price=avg")
                mock_display.assert_called_once_with("price", "avg", 75.0)

@pytest.mark.parametrize("exception_type,expected_message", [
    (FileNotFoundError, "Ошибка: файл 'test.csv' не найден"),
    (ValueError("Test error"), "Ошибка данных: Test error"),
    (KeyError("'price'"), "Ошибка: столбец \"'price'\" не найден в данных"),
    (RuntimeError("Unexpected"), "Неожиданная ошибка: Unexpected"),
])
def test_execute_handles_exceptions(capsys, exception_type, expected_message):
    """Тест обработки различных исключений в execute"""
    handler = CommandHandler()
    args = Arguments(filename="test.csv")
    
    with patch.object(handler.csv_reader, 'read_file') as mock_read:
        mock_read.side_effect = exception_type
        
        handler.execute(args)
        
        captured = capsys.readouterr()
        assert expected_message in captured.out

def test_execute_aggregate_parses_condition_correctly():
    """Тест что _execute_aggregate правильно парсит условие"""
    handler = CommandHandler()
    aggregate_condition = AggregateCondition(column="quantity", function=AggregateFunction.MAX)
    
    with patch.object(handler.csv_reader, 'read_file') as mock_read:
        with patch.object(handler.aggregator, 'aggregate_data') as mock_aggregate:
            with patch.object(handler.output_formatter, 'display_aggregate_result') as mock_display:
                mock_read.return_value = (["name", "price"], [])
                mock_aggregate.return_value = 100.0
                
                handler._execute_aggregate("test.csv", aggregate_condition)
                
                mock_display.assert_called_once_with("quantity", "max", 100.0)

def test_execute_methods_integration():
    """Тест интеграции всех методов execute"""
    handler = CommandHandler()
    
    with patch.object(handler, '_execute_filter') as mock_filter:
        with patch.object(handler, '_execute_aggregate') as mock_aggregate:
            with patch.object(handler.csv_reader, 'read_file'):
                with patch.object(handler.output_formatter, 'display_table'):
                    args = Arguments(filename="test.csv")
                    handler.execute(args)
                    mock_filter.assert_not_called()
                    mock_aggregate.assert_not_called()
    
    filter_condition = FilterCondition(column="price", operator=FilterOperator.GREATER, value="100")
    with patch.object(handler, '_execute_filter') as mock_filter:
        with patch.object(handler, '_execute_aggregate') as mock_aggregate:
            args = Arguments(filename="test.csv", filter_condition=filter_condition)
            handler.execute(args)
            mock_filter.assert_called_once()
            mock_aggregate.assert_not_called()
    
    aggregate_condition = AggregateCondition(column="price", function=AggregateFunction.AVG)
    with patch.object(handler, '_execute_filter') as mock_filter:
        with patch.object(handler, '_execute_aggregate') as mock_aggregate:
            args = Arguments(filename="test.csv", aggregate_condition=aggregate_condition)
            handler.execute(args)
            mock_filter.assert_not_called()
            mock_aggregate.assert_called_once() 