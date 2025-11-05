"""
Модуль View - содержит класс для отображения данных пользователю
"""

from typing import List
from model import Contact


class View:
    """Класс для отображения информации пользователю"""
    
    @staticmethod
    def show_menu():
        """Отображает главное меню"""
        print("\n" + "="*60)
        print("ТЕЛЕФОННЫЙ СПРАВОЧНИК")
        print("="*60)
        print("1. Открыть файл")
        print("2. Сохранить файл")
        print("3. Показать все контакты")
        print("4. Создать контакт")
        print("5. Найти контакт")
        print("6. Изменить контакт")
        print("7. Удалить контакт")
        print("8. Выход")
        print("="*60)
    
    @staticmethod
    def show_welcome():
        """Показывает приветственное сообщение"""
        print("Добро пожаловать в телефонный справочник!")
    
    @staticmethod
    def show_file_loaded(filename: str, count: int):
        """Показывает сообщение о загрузке файла"""
        print(f"\nНайден файл {filename}. Загружаю...")
        print(f"Загружено контактов: {count}")
    
    @staticmethod
    def show_file_not_found(filename: str):
        """Показывает сообщение о том, что файл не найден"""
        print(f"\nФайл {filename} не найден. Начните работу с пустым справочником или загрузите файл через меню.")
    
    @staticmethod
    def show_file_saved(filename: str):
        """Показывает сообщение о сохранении файла"""
        print(f"Справочник сохранен в файл {filename}")
    
    @staticmethod
    def show_all_contacts(contacts: List[Contact]):
        """Показывает все контакты"""
        if not contacts:
            print("Справочник пуст.")
            return
        
        print("\n" + "="*60)
        print("ВСЕ КОНТАКТЫ")
        print("="*60)
        for contact in contacts:
            print(contact)
        print("="*60 + "\n")
    
    @staticmethod
    def show_contact_created(contact: Contact):
        """Показывает сообщение о создании контакта"""
        print(f"\nКонтакт '{contact.name}' успешно создан с ID {contact.id}")
    
    @staticmethod
    def show_contact_updated(contact_id: int):
        """Показывает сообщение об обновлении контакта"""
        print(f"\nКонтакт с ID {contact_id} успешно изменен.")
    
    @staticmethod
    def show_contact_deleted(contact_id: int):
        """Показывает сообщение об удалении контакта"""
        print(f"Контакт с ID {contact_id} успешно удален.")
    
    @staticmethod
    def show_search_results(results: List[Contact]):
        """Показывает результаты поиска"""
        if results:
            print(f"\nНайдено контактов: {len(results)}")
            print("="*60)
            for contact in results:
                print(contact)
            print("="*60 + "\n")
        else:
            print("Контакты не найдены.")
    
    @staticmethod
    def show_contact(contact: Contact):
        """Показывает информацию о контакте"""
        print(contact)
    
    @staticmethod
    def show_error(message: str):
        """Показывает сообщение об ошибке"""
        print(f"Ошибка: {message}")
    
    @staticmethod
    def show_warning(message: str):
        """Показывает предупреждение"""
        print(f"Предупреждение: {message}")
    
    @staticmethod
    def show_info(message: str):
        """Показывает информационное сообщение"""
        print(message)
    
    @staticmethod
    def show_goodbye():
        """Показывает прощальное сообщение"""
        print("\nДо свидания!")
    
    @staticmethod
    def show_unsaved_changes_warning():
        """Показывает предупреждение о несохраненных изменениях"""
        print("\nВнимание: У вас есть несохраненные изменения!")
    
    # Методы для ввода данных
    @staticmethod
    def get_menu_choice() -> str:
        """Получает выбор пользователя из меню"""
        return input("\nВыберите действие (1-8): ").strip()
    
    @staticmethod
    def get_filename() -> str:
        """Получает имя файла от пользователя"""
        return input("Введите имя файла для загрузки: ").strip()
    
    @staticmethod
    def get_contact_name() -> str:
        """Получает имя контакта от пользователя"""
        return input("Введите имя: ").strip()
    
    @staticmethod
    def get_contact_phone() -> str:
        """Получает телефон контакта от пользователя"""
        return input("Введите телефон: ").strip()
    
    @staticmethod
    def get_contact_comment() -> str:
        """Получает комментарий контакта от пользователя"""
        return input("Введите комментарий (необязательно): ").strip()
    
    @staticmethod
    def get_contact_id() -> str:
        """Получает ID контакта от пользователя"""
        return input("\nВведите ID контакта: ").strip()
    
    @staticmethod
    def get_search_type() -> str:
        """Получает тип поиска от пользователя"""
        print("\nПоиск контакта")
        print("-" * 30)
        print("1. Поиск по имени")
        print("2. Поиск по телефону")
        print("3. Поиск по комментарию")
        print("4. Общий поиск (по всем полям)")
        return input("\nВыберите тип поиска (1-4): ").strip()
    
    @staticmethod
    def get_search_term() -> str:
        """Получает поисковый запрос от пользователя"""
        return input("Введите поисковый запрос: ").strip().lower()
    
    @staticmethod
    def get_edit_field(current_value: str, field_name: str) -> str:
        """Получает новое значение поля для редактирования"""
        return input(f"{field_name} [{current_value}]: ").strip()
    
    @staticmethod
    def get_confirmation(message: str) -> str:
        """Получает подтверждение от пользователя"""
        return input(f"\n{message} (да/нет): ").strip().lower()
    
    @staticmethod
    def show_create_contact_header():
        """Показывает заголовок для создания контакта"""
        print("\nСоздание нового контакта")
        print("-" * 30)
    
    @staticmethod
    def show_edit_contact_header(contact: Contact):
        """Показывает заголовок для редактирования контакта"""
        print(f"\nТекущие данные контакта:")
        print(contact)
        print("\nВведите новые данные (оставьте пустым, чтобы оставить без изменений):")
    
    @staticmethod
    def show_delete_contact_header(contact: Contact):
        """Показывает заголовок для удаления контакта"""
        print(f"\nКонтакт для удаления:")
        print(contact)
    
    @staticmethod
    def wait_for_enter():
        """Ждет нажатия Enter"""
        try:
            input("Нажмите Enter для продолжения...")
        except (EOFError, KeyboardInterrupt):
            pass

