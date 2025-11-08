"""
Тесты для файловых операций
"""

import pytest
import os
import json
from model import PhoneBook, Contact, FileHandler
from exceptions import FileCorruptedError, FileOperationError


class TestFileOperations:
    """Тесты для операций с файлами"""
    
    def test_load_nonexistent_file(self, temp_file):
        """Тест загрузки несуществующего файла"""
        # Удаляем файл если он существует
        import os
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        phonebook = PhoneBook(filename=temp_file)
        result = phonebook.load_from_file()
        assert result is True
        assert phonebook.count == 0
    
    def test_load_empty_file(self, temp_file):
        """Тест загрузки пустого файла"""
        data = {"contacts": []}
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        phonebook = PhoneBook(filename=temp_file)
        result = phonebook.load_from_file()
        assert result is True
        assert phonebook.count == 0
    
    def test_load_file_with_contacts(self, sample_json_data):
        """Тест загрузки файла с контактами"""
        phonebook = PhoneBook(filename=sample_json_data)
        result = phonebook.load_from_file()
        assert result is True
        assert phonebook.count == 2
    
    def test_load_file_with_invalid_contact(self, temp_file):
        """Тест загрузки файла с невалидным контактом"""
        data = {
            "contacts": [
                {"id": 1, "name": "Тест1", "phone": "111"},  # Валидный
                {"id": 2, "name": "", "phone": "222"},  # Невалидный (пустое имя)
                {"id": 3, "name": "Тест3", "phone": "333"}  # Валидный
            ]
        }
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        phonebook = PhoneBook(filename=temp_file)
        result = phonebook.load_from_file()
        # Должен загрузить только валидные контакты
        assert result is True
        assert phonebook.count == 2
    
    def test_load_file_missing_contacts_key(self, temp_file):
        """Тест загрузки файла без ключа contacts"""
        data = {"last_updated": "2024-01-01T12:00:00"}
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        phonebook = PhoneBook(filename=temp_file)
        result = phonebook.load_from_file()
        assert result is True
        assert phonebook.count == 0
    
    def test_save_file_creates_file(self, empty_phonebook, temp_file):
        """Тест что сохранение создает файл"""
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        empty_phonebook.filename = temp_file
        contact = Contact(name="Тест", phone="123")
        empty_phonebook.add_contact(contact)
        
        result = empty_phonebook.save_to_file()
        assert result is True
        assert os.path.exists(temp_file)
    
    def test_save_file_preserves_data(self, phonebook_with_contacts, temp_file):
        """Тест что сохранение сохраняет данные"""
        phonebook_with_contacts.filename = temp_file
        phonebook_with_contacts.save_to_file()
        
        # Загружаем обратно
        new_phonebook = PhoneBook(filename=temp_file)
        new_phonebook.load_from_file()
        
        assert new_phonebook.count == phonebook_with_contacts.count
        assert new_phonebook.contacts[0].name == phonebook_with_contacts.contacts[0].name
    
    def test_save_and_load_roundtrip(self, temp_file):
        """Тест полного цикла сохранения и загрузки"""
        phonebook1 = PhoneBook(filename=temp_file)
        contact1 = Contact(name="Тест1", phone="111")
        contact2 = Contact(name="Тест2", phone="222")
        phonebook1.add_contact(contact1)
        phonebook1.add_contact(contact2)
        phonebook1.save_to_file()
        
        phonebook2 = PhoneBook(filename=temp_file)
        phonebook2.load_from_file()
        
        assert phonebook2.count == 2
        assert phonebook2.contacts[0].name == "Тест1"
        assert phonebook2.contacts[1].name == "Тест2"
    
    def test_load_corrupted_json_file(self, temp_file):
        """Тест загрузки поврежденного JSON файла"""
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("невалидный json {")
        
        phonebook = PhoneBook(filename=temp_file)
        result = phonebook.load_from_file()
        assert result is False
    
    def test_file_handler_load_corrupted_json(self, temp_file):
        """Тест FileHandler с поврежденным JSON"""
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("{невалидный}")
        
        with pytest.raises(FileCorruptedError):
            FileHandler.load_from_file(temp_file)
    
    def test_save_with_special_characters(self, temp_file):
        """Тест сохранения контактов со специальными символами"""
        phonebook = PhoneBook(filename=temp_file)
        contact = Contact(
            name="Иван Иванов",
            phone="+7 (999) 123-45-67",
            comment="Тест с эмодзи 😀 и кириллицей"
        )
        phonebook.add_contact(contact)
        phonebook.save_to_file()
        
        # Загружаем обратно
        new_phonebook = PhoneBook(filename=temp_file)
        new_phonebook.load_from_file()
        
        assert new_phonebook.count == 1
        assert new_phonebook.contacts[0].comment == "Тест с эмодзи 😀 и кириллицей"
    
    def test_load_file_with_utf8_encoding(self, temp_file):
        """Тест загрузки файла с UTF-8 кодировкой"""
        data = {
            "contacts": [
                {"id": 1, "name": "Иван", "phone": "123", "comment": "Тест"}
            ]
        }
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        phonebook = PhoneBook(filename=temp_file)
        phonebook.load_from_file()
        
        assert phonebook.count == 1
        assert phonebook.contacts[0].name == "Иван"

