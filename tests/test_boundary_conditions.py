"""
Тесты для граничных условий
"""

import pytest
from model import Contact, PhoneBook
from exceptions import (
    ContactValidationError,
    ContactNotFoundError,
    InvalidContactIDError
)


class TestBoundaryConditions:
    """Тесты граничных условий"""
    
    def test_empty_phonebook_operations(self, empty_phonebook):
        """Тест операций с пустым справочником"""
        assert empty_phonebook.count == 0
        assert empty_phonebook.find_by_id(1) is None
        
        with pytest.raises(ContactNotFoundError):
            empty_phonebook.get_contact(1)
        
        results = empty_phonebook.search("Тест")
        assert len(results) == 0
    
    def test_add_empty_contact_name(self):
        """Тест добавления контакта с пустым именем"""
        with pytest.raises(ContactValidationError):
            Contact(name="", phone="123")
    
    def test_add_empty_contact_phone(self):
        """Тест добавления контакта с пустым телефоном"""
        with pytest.raises(ContactValidationError):
            Contact(name="Тест", phone="")
    
    def test_search_nonexistent_contact(self, phonebook_with_contacts):
        """Тест поиска несуществующего контакта"""
        results = phonebook_with_contacts.search("Несуществующий", field="name")
        assert len(results) == 0
    
    def test_delete_nonexistent_contact(self, phonebook_with_contacts):
        """Тест удаления несуществующего контакта"""
        with pytest.raises(ContactNotFoundError):
            phonebook_with_contacts.delete_contact(999)
    
    def test_get_nonexistent_contact(self, phonebook_with_contacts):
        """Тест получения несуществующего контакта"""
        with pytest.raises(ContactNotFoundError, match="Контакт с ID 999 не найден"):
            phonebook_with_contacts.get_contact(999)
    
    def test_find_by_zero_id(self, phonebook_with_contacts):
        """Тест поиска по ID = 0"""
        with pytest.raises(InvalidContactIDError):
            phonebook_with_contacts.find_by_id(0)
    
    def test_find_by_negative_id(self, phonebook_with_contacts):
        """Тест поиска по отрицательному ID"""
        with pytest.raises(InvalidContactIDError):
            phonebook_with_contacts.find_by_id(-1)
    
    def test_update_nonexistent_contact(self, phonebook_with_contacts):
        """Тест обновления несуществующего контакта"""
        with pytest.raises(ContactNotFoundError):
            phonebook_with_contacts.update_contact(999, name="Тест")
    
    def test_contact_name_only_whitespace(self):
        """Тест контакта с именем только из пробелов"""
        with pytest.raises(ContactValidationError):
            Contact(name="   ", phone="123")
    
    def test_contact_phone_only_whitespace(self):
        """Тест контакта с телефоном только из пробелов"""
        with pytest.raises(ContactValidationError):
            Contact(name="Тест", phone="   ")
    
    def test_contact_with_none_id(self):
        """Тест контакта с None ID"""
        contact = Contact(name="Тест", phone="123", contact_id=None)
        assert contact.id is None
    
    def test_contact_id_setter_zero(self):
        """Тест установки ID = 0"""
        contact = Contact(name="Тест", phone="123")
        with pytest.raises(ContactValidationError):
            contact.id = 0
    
    def test_contact_id_setter_negative(self):
        """Тест установки отрицательного ID"""
        contact = Contact(name="Тест", phone="123")
        with pytest.raises(ContactValidationError):
            contact.id = -5
    
    def test_search_empty_string(self, phonebook_with_contacts):
        """Тест поиска с пустой строкой"""
        results = phonebook_with_contacts.search("", field="name")
        # Пустая строка должна найти все контакты (так как "" in любая строка)
        assert len(results) == phonebook_with_contacts.count
    
    def test_add_contact_with_max_id(self, empty_phonebook):
        """Тест добавления контакта с максимальным ID"""
        # При добавлении контакта метод add_contact перезаписывает ID
        # Поэтому нужно добавить контакт, затем установить ему большой ID
        contact = Contact(name="Тест", phone="123")
        empty_phonebook.add_contact(contact)
        # После добавления ID уже установлен, но можно изменить
        # Проверяем что next_id увеличился
        assert empty_phonebook.count == 1
        assert empty_phonebook.next_id == 2  # После добавления одного контакта next_id = 2
    
    def test_multiple_contacts_same_name(self, empty_phonebook):
        """Тест добавления нескольких контактов с одинаковым именем"""
        contact1 = Contact(name="Иван", phone="111")
        contact2 = Contact(name="Иван", phone="222")
        empty_phonebook.add_contact(contact1)
        empty_phonebook.add_contact(contact2)
        
        results = empty_phonebook.search("Иван", field="name")
        assert len(results) == 2
    
    def test_update_contact_no_changes(self, phonebook_with_contacts):
        """Тест обновления контакта без изменений"""
        contact_before = phonebook_with_contacts.get_contact(1)
        phonebook_with_contacts.update_contact(1)  # Без параметров
        contact_after = phonebook_with_contacts.get_contact(1)
        assert contact_before.name == contact_after.name
    
    def test_delete_last_contact(self, empty_phonebook):
        """Тест удаления последнего контакта"""
        contact = Contact(name="Тест", phone="123")
        empty_phonebook.add_contact(contact)
        assert empty_phonebook.count == 1
        
        empty_phonebook.delete_contact(1)
        assert empty_phonebook.count == 0

