"""
    Модуль содержит пути к файлам-ресурсам:
        DirUi - пути к файлам (элементам) интерфейса
"""

import enum


class DirUi(enum.Enum):
    """Пути к файлам (элементам) интерфейса"""
    MAIN_WINDOW = 'res', 'ui', 'app_main.ui'
    TABLE_WINDOW = 'res', 'ui', 'table.ui'


class DirFont(enum.Enum):
    """Пути к файлам шрифтов"""
    MAIN_FONT = 'res', 'font', 'pt-serif_regular.ttf'
