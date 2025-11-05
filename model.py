"""
Модуль Model - содержит классы для работы с данными
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from exceptions import (
    ContactValidationError, 
    ContactNotFoundError, 
    FileOperationError, 
    FileCorruptedError,
    InvalidContactIDError
)


class DataClassMeta(type):
    """Кастомный метакласс для создания датакласса"""
    
    def __new__(cls, name, bases, namespace):
        # Добавляем метод __repr__ если его нет
        if '__repr__' not in namespace:
            def __repr__(self):
                attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
                return f'{name}({attrs})'
            namespace['__repr__'] = __repr__
        
        # Добавляем метод __eq__ если его нет
        if '__eq__' not in namespace:
            def __eq__(self, other):
                if not isinstance(other, self.__class__):
                    return False
                return self.__dict__ == other.__dict__
            namespace['__eq__'] = __eq__
        
        return super().__new__(cls, name, bases, namespace)


class Contact(metaclass=DataClassMeta):
    """Класс для представления контакта (кастомный датакласс)"""
    
    def __init__(self, name: str, phone: str, comment: str = "", contact_id: Optional[int] = None):
        self._id = contact_id
        self._name = name.strip()
        self._phone = phone.strip()
        self._comment = comment.strip()
        
        # Валидация при создании
        self._validate()
    
    def _validate(self):
        """Валидация данных контакта"""
        if not self._name:
            raise ContactValidationError("Имя контакта не может быть пустым")
        if not self._phone:
            raise ContactValidationError("Телефон контакта не может быть пустым")
    
    @property
    def id(self) -> Optional[int]:
        """Геттер для ID"""
        return self._id
    
    @id.setter
    def id(self, value: Optional[int]):
        """Сеттер для ID"""
        if value is not None and value <= 0:
            raise ContactValidationError("ID должен быть положительным числом")
        self._id = value
    
    @property
    def name(self) -> str:
        """Геттер для имени"""
        return self._name
    
    @name.setter
    def name(self, value: str):
        """Сеттер для имени"""
        value = value.strip()
        if not value:
            raise ContactValidationError("Имя не может быть пустым")
        self._name = value
    
    @property
    def phone(self) -> str:
        """Геттер для телефона"""
        return self._phone
    
    @phone.setter
    def phone(self, value: str):
        """Сеттер для телефона"""
        value = value.strip()
        if not value:
            raise ContactValidationError("Телефон не может быть пустым")
        self._phone = value
    
    @property
    def comment(self) -> str:
        """Геттер для комментария"""
        return self._comment
    
    @comment.setter
    def comment(self, value: str):
        """Сеттер для комментария"""
        self._comment = value.strip()
    
    def to_dict(self) -> Dict:
        """Преобразует контакт в словарь"""
        return {
            'id': self._id,
            'name': self._name,
            'phone': self._phone,
            'comment': self._comment
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        """Создает контакт из словаря"""
        if 'name' not in data or 'phone' not in data:
            raise ContactValidationError(
                f"Контакт должен содержать поля 'name' и 'phone'. Получено: {list(data.keys())}"
            )
        return cls(
            name=data['name'],
            phone=data['phone'],
            comment=data.get('comment', ''),
            contact_id=data.get('id')
        )
    
    def __str__(self) -> str:
        id_str = str(self._id) if self._id is not None else "Нет"
        return f"ID: {id_str} | {self._name} | {self._phone} | {self._comment}"


class FileHandler:
    """Класс для работы с файлами"""
    
    @staticmethod
    def load_from_file(filename: str) -> Dict:
        """Загружает данные из JSON файла"""
        if not os.path.exists(filename):
            return {'contacts': []}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError:
            raise FileCorruptedError(f"Файл {filename} поврежден или имеет неверный формат JSON")
        except Exception as e:
            raise FileOperationError(f"Ошибка при чтении файла {filename}: {e}")
    
    @staticmethod
    def save_to_file(filename: str, contacts: List[Contact]) -> bool:
        """Сохраняет контакты в JSON файл"""
        try:
            data = {
                'contacts': [contact.to_dict() for contact in contacts],
                'last_updated': datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            raise FileOperationError(f"Ошибка при сохранении файла {filename}: {e}")


class PhoneBook:
    """Класс для работы с телефонным справочником"""
    
    def __init__(self, filename: str = "phonebook.json"):
        self._filename = filename
        self._contacts: List[Contact] = []
        self._next_id = 1
        self._modified = False
    
    @property
    def filename(self) -> str:
        """Геттер для имени файла"""
        return self._filename
    
    @filename.setter
    def filename(self, value: str):
        """Сеттер для имени файла"""
        if not value or not isinstance(value, str):
            raise ValueError("Имя файла должно быть непустой строкой")
        self._filename = value
    
    @property
    def contacts(self) -> List[Contact]:
        """Геттер для списка контактов"""
        return self._contacts.copy()  # Возвращаем копию для защиты от изменений
    
    @property
    def next_id(self) -> int:
        """Геттер для следующего ID"""
        return self._next_id
    
    @property
    def modified(self) -> bool:
        """Геттер для флага изменений"""
        return self._modified
    
    @property
    def count(self) -> int:
        """Геттер для количества контактов"""
        return len(self._contacts)
    
    def load_from_file(self) -> bool:
        """Загружает контакты из файла"""
        try:
            data = FileHandler.load_from_file(self._filename)
            
            # Загружаем контакты с обработкой ошибок валидации
            contacts_list = []
            for i, contact_data in enumerate(data.get('contacts', [])):
                try:
                    contacts_list.append(Contact.from_dict(contact_data))
                except ContactValidationError as e:
                    print(f"Предупреждение: Пропущен некорректный контакт #{i+1}: {e}")
                    continue
            
            self._contacts = contacts_list
            
            # Определяем следующий ID и присваиваем ID контактам без него
            self._assign_missing_ids()
            
            self._modified = False
            return True
            
        except FileCorruptedError as e:
            print(f"Ошибка: {e}")
            return False
        except FileOperationError as e:
            print(f"Ошибка: {e}")
            return False
    
    def save_to_file(self) -> bool:
        """Сохраняет контакты в файл"""
        try:
            FileHandler.save_to_file(self._filename, self._contacts)
            self._modified = False
            return True
        except FileOperationError as e:
            print(f"Ошибка: {e}")
            return False
    
    def _assign_missing_ids(self):
        """Присваивает ID контактам, у которых его нет"""
        modified_by_id = False
        
        if self._contacts:
            # Находим максимальный ID среди контактов, у которых есть ID
            ids_with_values = [contact.id for contact in self._contacts if contact.id is not None]
            if ids_with_values:
                self._next_id = max(ids_with_values) + 1
            else:
                self._next_id = 1
            
            # Присваиваем ID всем контактам, у которых его нет
            for contact in self._contacts:
                if contact.id is None:
                    contact.id = self._next_id
                    self._next_id += 1
                    modified_by_id = True
        
        if modified_by_id:
            self._modified = True
    
    def add_contact(self, contact: Contact) -> Contact:
        """Добавляет новый контакт"""
        contact.id = self._next_id
        self._contacts.append(contact)
        self._next_id += 1
        self._modified = True
        return contact
    
    def find_by_id(self, contact_id: int) -> Optional[Contact]:
        """Находит контакт по ID"""
        if contact_id <= 0:
            raise InvalidContactIDError(f"ID должен быть положительным числом, получено: {contact_id}")
        
        for contact in self._contacts:
            if contact.id == contact_id:
                return contact
        return None
    
    def get_contact(self, contact_id: int) -> Contact:
        """Получает контакт по ID или выбрасывает исключение"""
        contact = self.find_by_id(contact_id)
        if contact is None:
            raise ContactNotFoundError(f"Контакт с ID {contact_id} не найден")
        return contact
    
    def update_contact(self, contact_id: int, **kwargs) -> Contact:
        """Обновляет контакт"""
        contact = self.get_contact(contact_id)
        
        if 'name' in kwargs:
            contact.name = kwargs['name']
        if 'phone' in kwargs:
            contact.phone = kwargs['phone']
        if 'comment' in kwargs:
            contact.comment = kwargs['comment']
        
        self._modified = True
        return contact
    
    def delete_contact(self, contact_id: int) -> bool:
        """Удаляет контакт"""
        contact = self.get_contact(contact_id)
        self._contacts.remove(contact)
        self._modified = True
        return True
    
    def search(self, search_term: str, field: Optional[str] = None) -> List[Contact]:
        """Поиск контактов"""
        search_term = search_term.lower()
        results = []
        
        for contact in self._contacts:
            if field is None:
                # Общий поиск
                if (search_term in contact.name.lower() or 
                    search_term in contact.phone.lower() or 
                    search_term in contact.comment.lower()):
                    results.append(contact)
            elif field == 'name':
                if search_term in contact.name.lower():
                    results.append(contact)
            elif field == 'phone':
                if search_term in contact.phone.lower():
                    results.append(contact)
            elif field == 'comment':
                if search_term in contact.comment.lower():
                    results.append(contact)
        
        return results
    
    def has_unsaved_changes(self) -> bool:
        """Проверяет наличие несохраненных изменений"""
        return self._modified

