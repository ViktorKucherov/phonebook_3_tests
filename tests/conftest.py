"""
Конфигурация и фикстуры для тестов
"""

import pytest
import os
import json
import tempfile
from pathlib import Path
from model import Contact, PhoneBook, FileHandler
from exceptions import ContactValidationError, ContactNotFoundError


@pytest.fixture
def temp_file():
    """Создает временный файл для тестов"""
    fd, path = tempfile.mkstemp(suffix='.json', prefix='test_')
    os.close(fd)
    yield path
    # Удаляем файл после теста
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def sample_contact():
    """Создает образец контакта"""
    return Contact(name="Иван Иванов", phone="+7 (999) 123-45-67", comment="Друг", contact_id=1)


@pytest.fixture
def sample_contacts():
    """Создает список образцов контактов"""
    return [
        Contact(name="Иван Иванов", phone="+7 (999) 123-45-67", comment="Друг", contact_id=1),
        Contact(name="Мария Петрова", phone="+7 (999) 234-56-78", comment="Коллега", contact_id=2),
        Contact(name="Петр Сидоров", phone="8-800-555-35-35", comment="Семья", contact_id=3),
    ]


@pytest.fixture
def empty_phonebook(temp_file):
    """Создает пустой справочник"""
    return PhoneBook(filename=temp_file)


@pytest.fixture
def phonebook_with_contacts(temp_file, sample_contacts):
    """Создает справочник с контактами"""
    phonebook = PhoneBook(filename=temp_file)
    for contact in sample_contacts:
        phonebook.add_contact(contact)
    return phonebook


@pytest.fixture
def sample_json_data(temp_file):
    """Создает JSON файл с тестовыми данными"""
    data = {
        "contacts": [
            {"id": 1, "name": "Тест1", "phone": "111", "comment": "ком1"},
            {"id": 2, "name": "Тест2", "phone": "222", "comment": "ком2"}
        ],
        "last_updated": "2024-01-01T12:00:00"
    }
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return temp_file

