"""
Кастомные исключения для телефонного справочника
"""


class PhoneBookException(Exception):
    """Базовое исключение для телефонного справочника"""
    pass


class ContactValidationError(PhoneBookException):
    """Исключение при валидации контакта"""
    pass


class ContactNotFoundError(PhoneBookException):
    """Исключение когда контакт не найден"""
    pass


class FileOperationError(PhoneBookException):
    """Исключение при работе с файлами"""
    pass


class FileNotFoundError(FileOperationError):
    """Исключение когда файл не найден"""
    pass


class FileCorruptedError(FileOperationError):
    """Исключение когда файл поврежден"""
    pass


class InvalidInputError(PhoneBookException):
    """Исключение при неверном вводе пользователя"""
    pass


class InvalidContactIDError(InvalidInputError):
    """Исключение при неверном ID контакта"""
    pass

