"""
Главный файл приложения телефонного справочника
Использует паттерн MVC
"""

from controller import Controller


def main():
    """Главная функция приложения"""
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()

