"""
Тесты для кастомных исключений
"""

import pytest
from exceptions import (
    PhoneBookException,
    ContactValidationError,
    ContactNotFoundError,
    FileOperationError,
    FileNotFoundError,
    FileCorruptedError,
    InvalidInputError,
    InvalidContactIDError
)


class TestExceptions:
    """Тесты для исключений"""
    
    def test_phonebook_exception_base(self):
        """Тест что PhoneBookException - базовое исключение"""
        assert issubclass(ContactValidationError, PhoneBookException)
        assert issubclass(ContactNotFoundError, PhoneBookException)
        assert issubclass(FileOperationError, PhoneBookException)
    
    def test_contact_validation_error(self):
        """Тест ContactValidationError"""
        error = ContactValidationError("Тестовая ошибка")
        assert str(error) == "Тестовая ошибка"
        assert isinstance(error, PhoneBookException)
    
    def test_contact_not_found_error(self):
        """Тест ContactNotFoundError"""
        error = ContactNotFoundError("Контакт не найден")
        assert str(error) == "Контакт не найден"
        assert isinstance(error, PhoneBookException)
    
    def test_file_operation_error(self):
        """Тест FileOperationError"""
        error = FileOperationError("Ошибка файла")
        assert str(error) == "Ошибка файла"
        assert isinstance(error, PhoneBookException)
    
    def test_file_not_found_error(self):
        """Тест FileNotFoundError"""
        error = FileNotFoundError("Файл не найден")
        assert str(error) == "Файл не найден"
        assert isinstance(error, FileOperationError)
        assert isinstance(error, PhoneBookException)
    
    def test_file_corrupted_error(self):
        """Тест FileCorruptedError"""
        error = FileCorruptedError("Файл поврежден")
        assert str(error) == "Файл поврежден"
        assert isinstance(error, FileOperationError)
        assert isinstance(error, PhoneBookException)
    
    def test_invalid_input_error(self):
        """Тест InvalidInputError"""
        error = InvalidInputError("Неверный ввод")
        assert str(error) == "Неверный ввод"
        assert isinstance(error, PhoneBookException)
    
    def test_invalid_contact_id_error(self):
        """Тест InvalidContactIDError"""
        error = InvalidContactIDError("Неверный ID")
        assert str(error) == "Неверный ID"
        assert isinstance(error, InvalidInputError)
        assert isinstance(error, PhoneBookException)

