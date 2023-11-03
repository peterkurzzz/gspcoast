"""
    Модуль редактирования общих сведений о КИП
"""

import os

from PyQt6 import uic
from PyQt6 import QtWidgets

from src.general_modules.resoursedir import DirUi


class ManagerDBCmd(QtWidgets.QWidget):
    """Главная таблица корректировки БД сведений о КИПиА"""
    def __init__(self):
        super().__init__()

        # Путь к файлу (элементу) интерфейса
        file_path = DirUi.TABLE_WINDOW.value

        # Загрузка файла (элемента) интерфейса
        uic.loadUi(os.path.join(*file_path), self)

