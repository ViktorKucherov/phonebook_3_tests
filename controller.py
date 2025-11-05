"""
Модуль Controller - содержит класс для управления логикой приложения
"""

import os
from model import PhoneBook, Contact
from view import View
from exceptions import (
    PhoneBookException,
    ContactValidationError,
    ContactNotFoundError,
    InvalidInputError,
    InvalidContactIDError,
    FileOperationError
)


class Controller:
    """Класс контроллера для управления приложением"""
    
    def __init__(self):
        self.phonebook = PhoneBook()
        self.view = View()
    
    def run(self):
        """Запускает главный цикл приложения"""
        self.view.show_welcome()
        
        # Пытаемся автоматически загрузить файл по умолчанию
        if os.path.exists(self.phonebook.filename):
            self.phonebook.load_from_file()
            self.view.show_file_loaded(self.phonebook.filename, self.phonebook.count)
        else:
            self.view.show_file_not_found(self.phonebook.filename)
        
        while True:
            self.view.show_menu()
            
            try:
                choice = self.view.get_menu_choice()
                
                if choice == "1":
                    self.handle_load_file()
                elif choice == "2":
                    self.handle_save_file()
                elif choice == "3":
                    self.handle_show_all()
                elif choice == "4":
                    self.handle_create_contact()
                elif choice == "5":
                    self.handle_find_contact()
                elif choice == "6":
                    self.handle_edit_contact()
                elif choice == "7":
                    self.handle_delete_contact()
                elif choice == "8":
                    self.handle_exit()
                    break
                else:
                    self.view.show_error("Неверный выбор. Пожалуйста, выберите действие от 1 до 8.")
            
            except KeyboardInterrupt:
                self.handle_interrupt()
                break
            except EOFError:
                self.handle_eof_error()
                break
            except PhoneBookException as e:
                self.view.show_error(str(e))
                self.view.wait_for_enter()
            except Exception as e:
                self.view.show_error(f"Произошла ошибка: {e}")
                self.view.wait_for_enter()
    
    def handle_load_file(self):
        """Обрабатывает загрузку файла"""
        try:
            filename = self.view.get_filename()
            if filename:
                self.phonebook.filename = filename
            if self.phonebook.load_from_file():
                self.view.show_file_loaded(self.phonebook.filename, self.phonebook.count)
        except Exception as e:
            self.view.show_error(str(e))
    
    def handle_save_file(self):
        """Обрабатывает сохранение файла"""
        try:
            if self.phonebook.save_to_file():
                self.view.show_file_saved(self.phonebook.filename)
        except Exception as e:
            self.view.show_error(str(e))
    
    def handle_show_all(self):
        """Обрабатывает отображение всех контактов"""
        self.view.show_all_contacts(self.phonebook.contacts)
    
    def handle_create_contact(self):
        """Обрабатывает создание контакта"""
        try:
            self.view.show_create_contact_header()
            
            name = self.view.get_contact_name()
            if not name:
                raise ContactValidationError("Имя не может быть пустым.")
            
            phone = self.view.get_contact_phone()
            if not phone:
                raise ContactValidationError("Телефон не может быть пустым.")
            
            # Валидация телефона
            if not self._validate_phone(phone):
                self.view.show_warning("Телефон может содержать только цифры, пробелы, +, -, (, )")
            
            comment = self.view.get_contact_comment()
            
            contact = Contact(name=name, phone=phone, comment=comment)
            created_contact = self.phonebook.add_contact(contact)
            self.view.show_contact_created(created_contact)
            
        except KeyboardInterrupt:
            self.view.show_info("\nОперация отменена.")
        except ContactValidationError as e:
            self.view.show_error(str(e))
    
    def handle_find_contact(self):
        """Обрабатывает поиск контакта"""
        if not self.phonebook.contacts:
            self.view.show_info("Справочник пуст.")
            return
        
        try:
            choice = self.view.get_search_type()
            search_term = self.view.get_search_term()
            
            if not search_term:
                raise InvalidInputError("Поисковый запрос не может быть пустым.")
            
            field_map = {
                "1": "name",
                "2": "phone",
                "3": "comment",
                "4": None
            }
            
            field = field_map.get(choice)
            if field is None and choice != "4":
                self.view.show_warning("Неверный выбор. Используется общий поиск.")
                field = None
            
            results = self.phonebook.search(search_term, field)
            self.view.show_search_results(results)
            
        except KeyboardInterrupt:
            self.view.show_info("\nОперация отменена.")
        except InvalidInputError as e:
            self.view.show_error(str(e))
    
    def handle_edit_contact(self):
        """Обрабатывает редактирование контакта"""
        if not self.phonebook.contacts:
            self.view.show_info("Справочник пуст.")
            return
        
        try:
            contact_id_str = self.view.get_contact_id()
            
            if not contact_id_str.isdigit():
                raise InvalidContactIDError("ID должен быть числом.")
            
            contact_id = int(contact_id_str)
            contact = self.phonebook.get_contact(contact_id)
            
            self.view.show_edit_contact_header(contact)
            
            new_name = self.view.get_edit_field(contact.name, "Имя")
            new_phone = self.view.get_edit_field(contact.phone, "Телефон")
            new_comment = self.view.get_edit_field(contact.comment, "Комментарий")
            
            # Обновляем только измененные поля
            update_data = {}
            if new_name:
                update_data['name'] = new_name
            if new_phone:
                if not self._validate_phone(new_phone):
                    self.view.show_warning("Телефон может содержать только цифры, пробелы, +, -, (, )")
                update_data['phone'] = new_phone
            if new_comment:
                update_data['comment'] = new_comment
            
            if update_data:
                self.phonebook.update_contact(contact_id, **update_data)
                self.view.show_contact_updated(contact_id)
            else:
                self.view.show_info("Изменения не внесены.")
            
        except KeyboardInterrupt:
            self.view.show_info("\nОперация отменена.")
        except (ContactNotFoundError, InvalidContactIDError) as e:
            self.view.show_error(str(e))
        except ContactValidationError as e:
            self.view.show_error(str(e))
    
    def handle_delete_contact(self):
        """Обрабатывает удаление контакта"""
        if not self.phonebook.contacts:
            self.view.show_info("Справочник пуст.")
            return
        
        try:
            contact_id_str = self.view.get_contact_id()
            
            if not contact_id_str.isdigit():
                raise InvalidContactIDError("ID должен быть числом.")
            
            contact_id = int(contact_id_str)
            contact = self.phonebook.get_contact(contact_id)
            
            self.view.show_delete_contact_header(contact)
            
            confirm = self.view.get_confirmation("Вы уверены?")
            
            if confirm in ['да', 'yes', 'y', 'д']:
                self.phonebook.delete_contact(contact_id)
                self.view.show_contact_deleted(contact_id)
            else:
                self.view.show_info("Удаление отменено.")
                
        except KeyboardInterrupt:
            self.view.show_info("\nОперация отменена.")
        except (ContactNotFoundError, InvalidContactIDError) as e:
            self.view.show_error(str(e))
    
    def handle_exit(self):
        """Обрабатывает выход из приложения"""
        if self.phonebook.has_unsaved_changes():
            try:
                save = self.view.get_confirmation("У вас есть несохраненные изменения. Сохранить?")
                if save in ['да', 'yes', 'y', 'д']:
                    self.phonebook.save_to_file()
                    self.view.show_file_saved(self.phonebook.filename)
            except (EOFError, KeyboardInterrupt):
                self.view.show_warning("\nИзменения не сохранены.")
        self.view.show_goodbye()
    
    def handle_interrupt(self):
        """Обрабатывает прерывание программы (Ctrl+C)"""
        self.view.show_info("\n\nПрерывание программы...")
        if self.phonebook.has_unsaved_changes():
            try:
                save = self.view.get_confirmation("У вас есть несохраненные изменения. Сохранить?")
                if save in ['да', 'yes', 'y', 'д']:
                    self.phonebook.save_to_file()
                    self.view.show_file_saved(self.phonebook.filename)
            except (EOFError, KeyboardInterrupt):
                self.view.show_warning("\nИзменения не сохранены.")
        self.view.show_goodbye()
    
    def handle_eof_error(self):
        """Обрабатывает ошибку EOF (отсутствие интерактивного ввода)"""
        self.view.show_error("\n\nНевозможно получить ввод от пользователя.")
        self.view.show_info("Программа требует интерактивного режима работы.")
        if self.phonebook.has_unsaved_changes():
            self.view.show_unsaved_changes_warning()
        self.view.show_goodbye()
    
    @staticmethod
    def _validate_phone(phone: str) -> bool:
        """Проверяет формат телефона"""
        allowed_chars = set('0123456789+-() ')
        return all(c in allowed_chars for c in phone)

