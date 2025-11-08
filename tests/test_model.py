"""
Тесты для модели данных (Contact, PhoneBook, FileHandler)
"""

import pytest
import os
import json
from model import Contact, PhoneBook, FileHandler
from exceptions import (
    ContactValidationError,
    ContactNotFoundError,
    InvalidContactIDError,
    FileOperationError,
    FileCorruptedError
)


class TestContact:
    """Тесты для класса Contact"""
    
    def test_contact_creation(self):
        """Тест создания контакта"""
        contact = Contact(name="Тест", phone="123", comment="комментарий", contact_id=1)
        assert contact.id == 1
        assert contact.name == "Тест"
        assert contact.phone == "123"
        assert contact.comment == "комментарий"
    
    def test_contact_creation_without_id(self):
        """Тест создания контакта без ID"""
        contact = Contact(name="Тест", phone="123")
        assert contact.id is None
        assert contact.name == "Тест"
        assert contact.phone == "123"
    
    def test_contact_empty_name_raises_error(self):
        """Тест что пустое имя вызывает ошибку"""
        with pytest.raises(ContactValidationError, match="Имя контакта не может быть пустым"):
            Contact(name="", phone="123")
    
    def test_contact_empty_phone_raises_error(self):
        """Тест что пустой телефон вызывает ошибку"""
        with pytest.raises(ContactValidationError, match="Телефон контакта не может быть пустым"):
            Contact(name="Тест", phone="")
    
    def test_contact_strips_whitespace(self):
        """Тест что пробелы обрезаются"""
        contact = Contact(name="  Тест  ", phone="  123  ", comment="  ком  ")
        assert contact.name == "Тест"
        assert contact.phone == "123"
        assert contact.comment == "ком"
    
    def test_contact_property_getters(self, sample_contact):
        """Тест геттеров свойств"""
        assert sample_contact.id == 1
        assert sample_contact.name == "Иван Иванов"
        assert sample_contact.phone == "+7 (999) 123-45-67"
        assert sample_contact.comment == "Друг"
    
    def test_contact_name_setter_valid(self):
        """Тест сеттера имени с валидным значением"""
        contact = Contact(name="Тест", phone="123")
        contact.name = "Новое имя"
        assert contact.name == "Новое имя"
    
    def test_contact_name_setter_empty_raises_error(self):
        """Тест что сеттер имени не принимает пустое значение"""
        contact = Contact(name="Тест", phone="123")
        with pytest.raises(ContactValidationError, match="Имя не может быть пустым"):
            contact.name = ""
    
    def test_contact_phone_setter_valid(self):
        """Тест сеттера телефона с валидным значением"""
        contact = Contact(name="Тест", phone="123")
        contact.phone = "+7 (999) 999-99-99"
        assert contact.phone == "+7 (999) 999-99-99"
    
    def test_contact_phone_setter_empty_raises_error(self):
        """Тест что сеттер телефона не принимает пустое значение"""
        contact = Contact(name="Тест", phone="123")
        with pytest.raises(ContactValidationError, match="Телефон не может быть пустым"):
            contact.phone = ""
    
    def test_contact_id_setter_valid(self):
        """Тест сеттера ID с валидным значением"""
        contact = Contact(name="Тест", phone="123")
        contact.id = 5
        assert contact.id == 5
    
    def test_contact_id_setter_invalid_raises_error(self):
        """Тест что сеттер ID не принимает отрицательное значение"""
        contact = Contact(name="Тест", phone="123")
        with pytest.raises(ContactValidationError, match="ID должен быть положительным числом"):
            contact.id = -1
    
    def test_contact_id_setter_zero_raises_error(self):
        """Тест что сеттер ID не принимает ноль"""
        contact = Contact(name="Тест", phone="123")
        with pytest.raises(ContactValidationError, match="ID должен быть положительным числом"):
            contact.id = 0
    
    def test_contact_id_setter_none_allowed(self):
        """Тест что сеттер ID принимает None"""
        contact = Contact(name="Тест", phone="123", contact_id=1)
        contact.id = None
        assert contact.id is None
    
    def test_contact_to_dict(self, sample_contact):
        """Тест преобразования контакта в словарь"""
        data = sample_contact.to_dict()
        assert data == {
            'id': 1,
            'name': 'Иван Иванов',
            'phone': '+7 (999) 123-45-67',
            'comment': 'Друг'
        }
    
    def test_contact_from_dict(self):
        """Тест создания контакта из словаря"""
        data = {'id': 1, 'name': 'Тест', 'phone': '123', 'comment': 'ком'}
        contact = Contact.from_dict(data)
        assert contact.id == 1
        assert contact.name == "Тест"
        assert contact.phone == "123"
        assert contact.comment == "ком"
    
    def test_contact_from_dict_missing_name_raises_error(self):
        """Тест что отсутствие имени в словаре вызывает ошибку"""
        data = {'phone': '123'}
        with pytest.raises(ContactValidationError):
            Contact.from_dict(data)
    
    def test_contact_from_dict_missing_phone_raises_error(self):
        """Тест что отсутствие телефона в словаре вызывает ошибку"""
        data = {'name': 'Тест'}
        with pytest.raises(ContactValidationError):
            Contact.from_dict(data)
    
    def test_contact_from_dict_optional_fields(self):
        """Тест что комментарий и ID опциональны"""
        data = {'name': 'Тест', 'phone': '123'}
        contact = Contact.from_dict(data)
        assert contact.comment == ""
        assert contact.id is None
    
    def test_contact_str_representation(self, sample_contact):
        """Тест строкового представления контакта"""
        str_repr = str(sample_contact)
        assert "ID: 1" in str_repr
        assert "Иван Иванов" in str_repr
        assert "+7 (999) 123-45-67" in str_repr
    
    def test_contact_str_with_none_id(self):
        """Тест строкового представления с None ID"""
        contact = Contact(name="Тест", phone="123", contact_id=None)
        str_repr = str(contact)
        assert "Нет" in str_repr or "None" in str_repr
    
    def test_contact_dataclass_repr(self):
        """Тест что кастомный датакласс имеет __repr__"""
        contact = Contact(name="Тест", phone="123", contact_id=1)
        repr_str = repr(contact)
        assert "Contact" in repr_str
        assert "Тест" in repr_str
    
    def test_contact_dataclass_eq(self):
        """Тест что кастомный датакласс имеет __eq__"""
        contact1 = Contact(name="Тест", phone="123", contact_id=1)
        contact2 = Contact(name="Тест", phone="123", contact_id=1)
        contact3 = Contact(name="Другой", phone="123", contact_id=1)
        assert contact1 == contact2
        assert contact1 != contact3


class TestFileHandler:
    """Тесты для класса FileHandler"""
    
    def test_load_from_existing_file(self, sample_json_data):
        """Тест загрузки из существующего файла"""
        data = FileHandler.load_from_file(sample_json_data)
        assert 'contacts' in data
        assert len(data['contacts']) == 2
        assert data['contacts'][0]['name'] == "Тест1"
    
    def test_load_from_nonexistent_file(self, temp_file):
        """Тест загрузки из несуществующего файла"""
        os.remove(temp_file)  # Удаляем файл
        data = FileHandler.load_from_file(temp_file)
        assert data == {'contacts': []}
    
    def test_load_corrupted_json_raises_error(self, temp_file):
        """Тест что поврежденный JSON вызывает ошибку"""
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("невалидный json {")
        with pytest.raises(FileCorruptedError):
            FileHandler.load_from_file(temp_file)
    
    def test_save_to_file(self, temp_file, sample_contacts):
        """Тест сохранения в файл"""
        result = FileHandler.save_to_file(temp_file, sample_contacts)
        assert result is True
        assert os.path.exists(temp_file)
        
        # Проверяем содержимое
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert 'contacts' in data
        assert len(data['contacts']) == 3
    
    def test_save_creates_file_if_not_exists(self, temp_file):
        """Тест что сохранение создает файл если его нет"""
        os.remove(temp_file)
        contact = Contact(name="Тест", phone="123")
        result = FileHandler.save_to_file(temp_file, [contact])
        assert result is True
        assert os.path.exists(temp_file)


class TestPhoneBook:
    """Тесты для класса PhoneBook"""
    
    def test_phonebook_initialization(self, temp_file):
        """Тест инициализации справочника"""
        phonebook = PhoneBook(filename=temp_file)
        assert phonebook.filename == temp_file
        assert phonebook.count == 0
        assert phonebook.next_id == 1
        assert phonebook.modified is False
    
    def test_phonebook_filename_property(self, temp_file):
        """Тест свойства filename"""
        phonebook = PhoneBook(filename=temp_file)
        new_filename = "new_file.json"
        phonebook.filename = new_filename
        assert phonebook.filename == new_filename
    
    def test_phonebook_filename_setter_invalid(self, temp_file):
        """Тест что невалидное имя файла вызывает ошибку"""
        phonebook = PhoneBook(filename=temp_file)
        with pytest.raises(ValueError, match="Имя файла должно быть непустой строкой"):
            phonebook.filename = ""
    
    def test_phonebook_add_contact(self, empty_phonebook, sample_contact):
        """Тест добавления контакта"""
        contact = empty_phonebook.add_contact(sample_contact)
        assert contact.id is not None
        assert empty_phonebook.count == 1
        assert empty_phonebook.modified is True
        assert contact in empty_phonebook.contacts
    
    def test_phonebook_add_contact_auto_id(self, empty_phonebook):
        """Тест что ID присваивается автоматически"""
        contact = Contact(name="Тест", phone="123")
        added = empty_phonebook.add_contact(contact)
        assert added.id == 1
        assert empty_phonebook.next_id == 2
    
    def test_phonebook_add_multiple_contacts(self, empty_phonebook):
        """Тест добавления нескольких контактов"""
        contact1 = Contact(name="Тест1", phone="111")
        contact2 = Contact(name="Тест2", phone="222")
        empty_phonebook.add_contact(contact1)
        empty_phonebook.add_contact(contact2)
        assert empty_phonebook.count == 2
        assert empty_phonebook.next_id == 3
    
    def test_phonebook_find_by_id_existing(self, phonebook_with_contacts):
        """Тест поиска существующего контакта по ID"""
        contact = phonebook_with_contacts.find_by_id(1)
        assert contact is not None
        assert contact.id == 1
        assert contact.name == "Иван Иванов"
    
    def test_phonebook_find_by_id_nonexistent(self, phonebook_with_contacts):
        """Тест поиска несуществующего контакта"""
        contact = phonebook_with_contacts.find_by_id(999)
        assert contact is None
    
    def test_phonebook_find_by_id_invalid_raises_error(self, phonebook_with_contacts):
        """Тест что невалидный ID вызывает ошибку"""
        with pytest.raises(InvalidContactIDError):
            phonebook_with_contacts.find_by_id(0)
        with pytest.raises(InvalidContactIDError):
            phonebook_with_contacts.find_by_id(-1)
    
    def test_phonebook_get_contact_existing(self, phonebook_with_contacts):
        """Тест получения существующего контакта"""
        contact = phonebook_with_contacts.get_contact(1)
        assert contact.id == 1
    
    def test_phonebook_get_contact_nonexistent_raises_error(self, phonebook_with_contacts):
        """Тест что получение несуществующего контакта вызывает ошибку"""
        with pytest.raises(ContactNotFoundError, match="Контакт с ID 999 не найден"):
            phonebook_with_contacts.get_contact(999)
    
    def test_phonebook_update_contact(self, phonebook_with_contacts):
        """Тест обновления контакта"""
        updated = phonebook_with_contacts.update_contact(1, name="Новое имя")
        assert updated.name == "Новое имя"
        assert phonebook_with_contacts.modified is True
        
        # Проверяем что изменения сохранились
        contact = phonebook_with_contacts.get_contact(1)
        assert contact.name == "Новое имя"
    
    def test_phonebook_update_contact_multiple_fields(self, phonebook_with_contacts):
        """Тест обновления нескольких полей"""
        updated = phonebook_with_contacts.update_contact(
            1, 
            name="Новое имя", 
            phone="999-999-99-99",
            comment="Новый комментарий"
        )
        contact = phonebook_with_contacts.get_contact(1)
        assert contact.name == "Новое имя"
        assert contact.phone == "999-999-99-99"
        assert contact.comment == "Новый комментарий"
    
    def test_phonebook_update_contact_nonexistent_raises_error(self, phonebook_with_contacts):
        """Тест что обновление несуществующего контакта вызывает ошибку"""
        with pytest.raises(ContactNotFoundError):
            phonebook_with_contacts.update_contact(999, name="Тест")
    
    def test_phonebook_delete_contact(self, phonebook_with_contacts):
        """Тест удаления контакта"""
        result = phonebook_with_contacts.delete_contact(1)
        assert result is True
        assert phonebook_with_contacts.count == 2
        assert phonebook_with_contacts.modified is True
        
        # Проверяем что контакт удален
        with pytest.raises(ContactNotFoundError):
            phonebook_with_contacts.get_contact(1)
    
    def test_phonebook_delete_contact_nonexistent_raises_error(self, phonebook_with_contacts):
        """Тест что удаление несуществующего контакта вызывает ошибку"""
        with pytest.raises(ContactNotFoundError):
            phonebook_with_contacts.delete_contact(999)
    
    def test_phonebook_search_by_name(self, phonebook_with_contacts):
        """Тест поиска по имени"""
        results = phonebook_with_contacts.search("Иван", field="name")
        assert len(results) == 1
        assert results[0].name == "Иван Иванов"
    
    def test_phonebook_search_by_phone(self, phonebook_with_contacts):
        """Тест поиска по телефону"""
        results = phonebook_with_contacts.search("123-45-67", field="phone")
        assert len(results) == 1
        assert results[0].phone == "+7 (999) 123-45-67"
    
    def test_phonebook_search_by_comment(self, phonebook_with_contacts):
        """Тест поиска по комментарию"""
        results = phonebook_with_contacts.search("Друг", field="comment")
        assert len(results) == 1
        assert results[0].comment == "Друг"
    
    def test_phonebook_search_general(self, phonebook_with_contacts):
        """Тест общего поиска"""
        results = phonebook_with_contacts.search("Иван")
        assert len(results) == 1
    
    def test_phonebook_search_case_insensitive(self, phonebook_with_contacts):
        """Тест что поиск не чувствителен к регистру"""
        results = phonebook_with_contacts.search("ИВАН", field="name")
        assert len(results) == 1
    
    def test_phonebook_search_no_results(self, phonebook_with_contacts):
        """Тест поиска без результатов"""
        results = phonebook_with_contacts.search("Несуществующий", field="name")
        assert len(results) == 0
    
    def test_phonebook_load_from_file(self, sample_json_data):
        """Тест загрузки из файла"""
        phonebook = PhoneBook(filename=sample_json_data)
        result = phonebook.load_from_file()
        assert result is True
        assert phonebook.count == 2
        assert phonebook.next_id == 3  # max(1, 2) + 1
    
    def test_phonebook_load_assigns_missing_ids(self, temp_file):
        """Тест что загрузка присваивает отсутствующие ID"""
        data = {
            "contacts": [
                {"name": "Тест1", "phone": "111"},
                {"id": 5, "name": "Тест2", "phone": "222"},
                {"name": "Тест3", "phone": "333"}
            ]
        }
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        phonebook = PhoneBook(filename=temp_file)
        phonebook.load_from_file()
        assert phonebook.count == 3
        # Контакт без ID должен получить ID = 6 (max(5) + 1)
        contacts = phonebook.contacts
        ids = [c.id for c in contacts]
        assert None not in ids
        assert 6 in ids
    
    def test_phonebook_save_to_file(self, phonebook_with_contacts, temp_file):
        """Тест сохранения в файл"""
        phonebook_with_contacts.filename = temp_file
        result = phonebook_with_contacts.save_to_file()
        assert result is True
        assert phonebook_with_contacts.modified is False
        assert os.path.exists(temp_file)
        
        # Проверяем содержимое
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data['contacts']) == 3
    
    def test_phonebook_has_unsaved_changes(self, empty_phonebook):
        """Тест проверки несохраненных изменений"""
        assert empty_phonebook.has_unsaved_changes() is False
        contact = Contact(name="Тест", phone="123")
        empty_phonebook.add_contact(contact)
        assert empty_phonebook.has_unsaved_changes() is True
    
    def test_phonebook_contacts_property_returns_copy(self, phonebook_with_contacts):
        """Тест что свойство contacts возвращает копию"""
        contacts = phonebook_with_contacts.contacts
        original_count = phonebook_with_contacts.count
        contacts.append(Contact(name="Новый", phone="999"))
        # Оригинальный список не должен измениться
        assert phonebook_with_contacts.count == original_count

