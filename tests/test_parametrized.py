"""
Параметризованные тесты для расширенной проверки
"""

import pytest
from model import Contact, PhoneBook
from exceptions import ContactValidationError, InvalidContactIDError


class TestParametrizedContactCreation:
    """Параметризованные тесты создания контактов"""
    
    @pytest.mark.parametrize("name,phone,comment,expected_name,expected_phone", [
        ("Иван Иванов", "+7 (999) 123-45-67", "Друг", "Иван Иванов", "+7 (999) 123-45-67"),
        ("Мария", "8-800-555-35-35", "", "Мария", "8-800-555-35-35"),
        ("Петр", "1234567890", "Работа", "Петр", "1234567890"),
        ("Анна", "+1 (555) 123-4567", "Семья", "Анна", "+1 (555) 123-4567"),
    ])
    def test_create_contact_valid_formats(self, name, phone, comment, expected_name, expected_phone):
        """Тест создания контактов с различными форматами"""
        contact = Contact(name=name, phone=phone, comment=comment)
        assert contact.name == expected_name
        assert contact.phone == expected_phone
        assert contact.comment == comment
    
    @pytest.mark.parametrize("name,phone", [
        ("", "123"),
        ("   ", "123"),
        ("Тест", ""),
        ("Тест", "   "),
        ("", ""),
    ])
    def test_create_contact_invalid_empty_fields(self, name, phone):
        """Тест что пустые поля вызывают ошибку"""
        with pytest.raises(ContactValidationError):
            Contact(name=name, phone=phone)
    
    @pytest.mark.parametrize("name,phone,id_value", [
        ("Тест1", "111", 1),
        ("Тест2", "222", 100),
        ("Тест3", "333", None),
    ])
    def test_contact_with_different_ids(self, name, phone, id_value):
        """Тест контактов с разными ID"""
        contact = Contact(name=name, phone=phone, contact_id=id_value)
        assert contact.id == id_value


class TestParametrizedPhoneBookOperations:
    """Параметризованные тесты операций со справочником"""
    
    @pytest.mark.parametrize("contact_count", [0, 1, 5, 10])
    def test_add_multiple_contacts(self, empty_phonebook, contact_count):
        """Тест добавления разного количества контактов"""
        for i in range(contact_count):
            contact = Contact(name=f"Тест{i}", phone=f"{i}{i}{i}")
            empty_phonebook.add_contact(contact)
        assert empty_phonebook.count == contact_count
    
    @pytest.mark.parametrize("search_term,field,expected_count", [
        ("Иван", "name", 1),
        ("иван", "name", 1),  # Нечувствительность к регистру
        ("123", "phone", 1),
        ("Мария", "name", 1),
        ("Несуществующий", "name", 0),
    ])
    def test_search_various_terms(self, phonebook_with_contacts, search_term, field, expected_count):
        """Тест поиска с различными запросами"""
        results = phonebook_with_contacts.search(search_term, field=field)
        assert len(results) == expected_count
    
    @pytest.mark.parametrize("contact_id,should_exist,should_raise", [
        (1, True, False),
        (2, True, False),
        (3, True, False),
        (999, False, False),  # Несуществующий, но валидный ID
        (0, False, True),  # Невалидный ID - выбрасывает исключение
        (-1, False, True),  # Невалидный ID - выбрасывает исключение
    ])
    def test_find_by_id_various(self, phonebook_with_contacts, contact_id, should_exist, should_raise):
        """Тест поиска по различным ID"""
        if should_raise:
            # Для невалидных ID должно быть исключение
            with pytest.raises(InvalidContactIDError):
                phonebook_with_contacts.find_by_id(contact_id)
        else:
            contact = phonebook_with_contacts.find_by_id(contact_id)
            if should_exist:
                assert contact is not None
                assert contact.id == contact_id
            else:
                assert contact is None


class TestParametrizedContactProperties:
    """Параметризованные тесты свойств контакта"""
    
    @pytest.mark.parametrize("original_name,new_name,should_succeed", [
        ("Иван", "Петр", True),
        ("Мария", "Анна", True),
        ("Тест", "", False),  # Пустое имя
        ("Тест", "   ", False),  # Только пробелы
    ])
    def test_name_setter_various_values(self, original_name, new_name, should_succeed):
        """Тест сеттера имени с различными значениями"""
        contact = Contact(name=original_name, phone="123")
        if should_succeed:
            contact.name = new_name
            assert contact.name == new_name.strip()
        else:
            with pytest.raises(ContactValidationError):
                contact.name = new_name
    
    @pytest.mark.parametrize("original_phone,new_phone,should_succeed", [
        ("123", "456", True),
        ("+7 (999) 123-45-67", "8-800-555-35-35", True),
        ("123", "", False),  # Пустой телефон
        ("123", "   ", False),  # Только пробелы
    ])
    def test_phone_setter_various_values(self, original_phone, new_phone, should_succeed):
        """Тест сеттера телефона с различными значениями"""
        contact = Contact(name="Тест", phone=original_phone)
        if should_succeed:
            contact.phone = new_phone
            assert contact.phone == new_phone.strip()
        else:
            with pytest.raises(ContactValidationError):
                contact.phone = new_phone
    
    @pytest.mark.parametrize("id_value,should_succeed", [
        (1, True),
        (100, True),
        (None, True),
        (0, False),  # Ноль
        (-1, False),  # Отрицательное
        (-100, False),  # Большое отрицательное
    ])
    def test_id_setter_various_values(self, id_value, should_succeed):
        """Тест сеттера ID с различными значениями"""
        contact = Contact(name="Тест", phone="123")
        if should_succeed:
            contact.id = id_value
            assert contact.id == id_value
        else:
            with pytest.raises(ContactValidationError):
                contact.id = id_value


class TestParametrizedEdgeCases:
    """Параметризованные тесты граничных условий"""
    
    @pytest.mark.parametrize("name_variations", [
        "A",  # Минимальная длина
        "А" * 100,  # Длинное имя
        "Иван-Петр",  # С дефисом
        "Мария О'Коннор",  # С апострофом
        "Жан-Пьер де Ла Фонтен",  # С пробелами и дефисами
    ])
    def test_contact_name_edge_cases(self, name_variations):
        """Тест граничных случаев для имени"""
        contact = Contact(name=name_variations, phone="123")
        assert contact.name == name_variations.strip()
    
    @pytest.mark.parametrize("phone_variations", [
        "1",  # Минимальная длина
        "+7 (999) 123-45-67",  # С форматом
        "8-800-555-35-35",  # С дефисами
        "12345678901234567890",  # Длинный номер
        "+1-555-123-4567",  # Международный формат
    ])
    def test_contact_phone_edge_cases(self, phone_variations):
        """Тест граничных случаев для телефона"""
        contact = Contact(name="Тест", phone=phone_variations)
        assert contact.phone == phone_variations.strip()
    
    @pytest.mark.parametrize("comment_variations", [
        "",  # Пустой комментарий
        " " * 10,  # Только пробелы
        "Обычный комментарий",  # Обычный
        "Комментарий\nс\nпереносами",  # С переносами
        "A" * 1000,  # Очень длинный
    ])
    def test_contact_comment_edge_cases(self, comment_variations):
        """Тест граничных случаев для комментария"""
        contact = Contact(name="Тест", phone="123", comment=comment_variations)
        assert contact.comment == comment_variations.strip()

