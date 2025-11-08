"""
Тесты для контроллера
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from controller import Controller
from model import Contact, PhoneBook
from exceptions import (
    ContactValidationError,
    ContactNotFoundError,
    InvalidContactIDError,
    InvalidInputError
)


class TestController:
    """Тесты для класса Controller"""
    
    @pytest.fixture
    def controller(self):
        """Создает контроллер для тестов"""
        return Controller()
    
    def test_controller_initialization(self, controller):
        """Тест инициализации контроллера"""
        assert controller.phonebook is not None
        assert controller.view is not None
        assert isinstance(controller.phonebook, PhoneBook)
    
    @patch('controller.View')
    @patch('controller.PhoneBook')
    def test_handle_create_contact_valid(self, mock_phonebook, mock_view, controller):
        """Тест создания валидного контакта"""
        # Настраиваем моки
        mock_view_instance = Mock()
        mock_view_instance.get_contact_name.return_value = "Тест"
        mock_view_instance.get_contact_phone.return_value = "123"
        mock_view_instance.get_contact_comment.return_value = "комментарий"
        controller.view = mock_view_instance
        
        mock_pb = Mock()
        mock_contact = Contact(name="Тест", phone="123", comment="комментарий")
        mock_pb.add_contact.return_value = mock_contact
        controller.phonebook = mock_pb
        
        controller.handle_create_contact()
        
        mock_pb.add_contact.assert_called_once()
        mock_view_instance.show_contact_created.assert_called_once_with(mock_contact)
    
    @patch('controller.View')
    def test_handle_create_contact_empty_name(self, mock_view, controller):
        """Тест создания контакта с пустым именем"""
        mock_view_instance = Mock()
        mock_view_instance.get_contact_name.return_value = ""
        controller.view = mock_view_instance
        
        # Контроллер обрабатывает ошибку через try-except, не выбрасывает наружу
        controller.handle_create_contact()
        mock_view_instance.show_error.assert_called()
    
    @patch('controller.View')
    def test_handle_create_contact_empty_phone(self, mock_view, controller):
        """Тест создания контакта с пустым телефоном"""
        mock_view_instance = Mock()
        mock_view_instance.get_contact_name.return_value = "Тест"
        mock_view_instance.get_contact_phone.return_value = ""
        controller.view = mock_view_instance
        
        # Контроллер обрабатывает ошибку через try-except, не выбрасывает наружу
        controller.handle_create_contact()
        mock_view_instance.show_error.assert_called()
    
    def test_handle_show_all_empty(self, controller):
        """Тест показа всех контактов при пустом справочнике"""
        controller.view = Mock()
        # Нельзя установить contacts напрямую, это readonly property
        # Вместо этого используем пустой справочник
        controller.phonebook._contacts = []
        controller.handle_show_all()
        controller.view.show_all_contacts.assert_called_once()
        # Проверяем что передали пустой список
        call_args = controller.view.show_all_contacts.call_args[0][0]
        assert len(call_args) == 0
    
    def test_handle_show_all_with_contacts(self, controller, sample_contacts):
        """Тест показа всех контактов"""
        controller.view = Mock()
        controller.phonebook._contacts = sample_contacts
        controller.handle_show_all()
        controller.view.show_all_contacts.assert_called_once()
    
    @patch('controller.View')
    def test_handle_find_contact_by_name(self, mock_view, controller, phonebook_with_contacts):
        """Тест поиска контакта по имени"""
        controller.phonebook = phonebook_with_contacts
        mock_view_instance = Mock()
        mock_view_instance.get_search_type.return_value = "1"
        mock_view_instance.get_search_term.return_value = "Иван"
        controller.view = mock_view_instance
        
        controller.handle_find_contact()
        
        mock_view_instance.show_search_results.assert_called_once()
        results = mock_view_instance.show_search_results.call_args[0][0]
        assert len(results) == 1
        assert results[0].name == "Иван Иванов"
    
    @patch('controller.View')
    def test_handle_find_contact_empty_query(self, mock_view, controller, phonebook_with_contacts):
        """Тест поиска с пустым запросом"""
        controller.phonebook = phonebook_with_contacts
        mock_view_instance = Mock()
        mock_view_instance.get_search_type.return_value = "1"
        mock_view_instance.get_search_term.return_value = ""
        controller.view = mock_view_instance
        
        # Контроллер обрабатывает ошибку через try-except, не выбрасывает наружу
        controller.handle_find_contact()
        mock_view_instance.show_error.assert_called()
    
    @patch('controller.View')
    def test_handle_edit_contact_valid(self, mock_view, controller, phonebook_with_contacts):
        """Тест редактирования контакта"""
        controller.phonebook = phonebook_with_contacts
        mock_view_instance = Mock()
        mock_view_instance.get_contact_id.return_value = "1"
        mock_view_instance.get_edit_field.side_effect = ["Новое имя", "", ""]
        controller.view = mock_view_instance
        
        controller.handle_edit_contact()
        
        contact = controller.phonebook.get_contact(1)
        assert contact.name == "Новое имя"
        mock_view_instance.show_contact_updated.assert_called_once_with(1)
    
    @patch('controller.View')
    def test_handle_edit_contact_invalid_id(self, mock_view, controller, phonebook_with_contacts):
        """Тест редактирования с невалидным ID"""
        controller.phonebook = phonebook_with_contacts
        mock_view_instance = Mock()
        mock_view_instance.get_contact_id.return_value = "abc"
        controller.view = mock_view_instance
        
        # Контроллер обрабатывает ошибку через try-except, не выбрасывает наружу
        controller.handle_edit_contact()
        mock_view_instance.show_error.assert_called()
    
    @patch('controller.View')
    def test_handle_edit_contact_nonexistent(self, mock_view, controller, phonebook_with_contacts):
        """Тест редактирования несуществующего контакта"""
        controller.phonebook = phonebook_with_contacts
        mock_view_instance = Mock()
        mock_view_instance.get_contact_id.return_value = "999"
        controller.view = mock_view_instance
        
        # Контроллер обрабатывает ошибку через try-except, не выбрасывает наружу
        controller.handle_edit_contact()
        mock_view_instance.show_error.assert_called()
    
    @patch('controller.View')
    def test_handle_delete_contact_with_confirmation(self, mock_view, controller, phonebook_with_contacts):
        """Тест удаления контакта с подтверждением"""
        controller.phonebook = phonebook_with_contacts
        mock_view_instance = Mock()
        mock_view_instance.get_contact_id.return_value = "1"
        mock_view_instance.get_confirmation.return_value = "да"
        controller.view = mock_view_instance
        
        initial_count = controller.phonebook.count
        controller.handle_delete_contact()
        
        assert controller.phonebook.count == initial_count - 1
        mock_view_instance.show_contact_deleted.assert_called_once_with(1)
    
    @patch('controller.View')
    def test_handle_delete_contact_without_confirmation(self, mock_view, controller, phonebook_with_contacts):
        """Тест отмены удаления контакта"""
        controller.phonebook = phonebook_with_contacts
        mock_view_instance = Mock()
        mock_view_instance.get_contact_id.return_value = "1"
        mock_view_instance.get_confirmation.return_value = "нет"
        controller.view = mock_view_instance
        
        initial_count = controller.phonebook.count
        controller.handle_delete_contact()
        
        assert controller.phonebook.count == initial_count  # Не изменилось
        mock_view_instance.show_info.assert_called()
    
    @patch('controller.View')
    def test_handle_save_file(self, mock_view, controller, phonebook_with_contacts, temp_file):
        """Тест сохранения файла"""
        controller.phonebook = phonebook_with_contacts
        controller.phonebook.filename = temp_file
        controller.view = Mock()
        
        controller.handle_save_file()
        
        assert controller.phonebook.modified is False
        controller.view.show_file_saved.assert_called_once()
    
    @patch('controller.View')
    def test_handle_load_file(self, mock_view, controller, sample_json_data):
        """Тест загрузки файла"""
        mock_view_instance = Mock()
        mock_view_instance.get_filename.return_value = ""  # Не меняем имя файла
        controller.view = mock_view_instance
        
        # Устанавливаем имя файла перед вызовом handle_load_file
        controller.phonebook.filename = sample_json_data
        
        # Проверяем что файл существует и содержит данные
        import os
        assert os.path.exists(sample_json_data)
        
        controller.handle_load_file()
        
        # После загрузки должно быть 2 контакта
        assert controller.phonebook.count == 2
        mock_view_instance.show_file_loaded.assert_called_once()
    
    @patch('controller.View')
    def test_handle_exit_with_unsaved_changes_save(self, mock_view, controller, phonebook_with_contacts, temp_file):
        """Тест выхода с сохранением изменений"""
        controller.phonebook = phonebook_with_contacts
        controller.phonebook.filename = temp_file
        controller.phonebook._modified = True
        mock_view_instance = Mock()
        mock_view_instance.get_confirmation.return_value = "да"
        controller.view = mock_view_instance
        
        controller.handle_exit()
        
        mock_view_instance.show_file_saved.assert_called_once()
        mock_view_instance.show_goodbye.assert_called_once()
    
    @patch('controller.View')
    def test_handle_exit_with_unsaved_changes_no_save(self, mock_view, controller, phonebook_with_contacts):
        """Тест выхода без сохранения изменений"""
        controller.phonebook = phonebook_with_contacts
        controller.phonebook._modified = True
        mock_view_instance = Mock()
        mock_view_instance.get_confirmation.return_value = "нет"
        controller.view = mock_view_instance
        
        controller.handle_exit()
        
        mock_view_instance.show_goodbye.assert_called_once()
    
    @patch('controller.View')
    def test_handle_exit_no_changes(self, mock_view, controller, phonebook_with_contacts):
        """Тест выхода без изменений"""
        controller.phonebook = phonebook_with_contacts
        controller.phonebook._modified = False
        controller.view = Mock()
        
        controller.handle_exit()
        
        controller.view.show_goodbye.assert_called_once()

