"""
    Модуль для открытия файла (элемента) интерфейса с расширением .ui.
    Задаваемые параметры - элементы дерева каталогов и имя файла (string)
"""
import os

from PyQt6 import uic
from PyQt6 import QtWidgets


class OpenUi(QtWidgets.QWidget):
    def __init__(self, *args):
        super().__init__()
    #   Формирование пути к файлу интерфейса
        ui_file = os.path.join(*args)
    #     print(ui_file)
    #
    #     #   Создание объекта интерфейса из файла
    #     # Form, Base = uic.loadUiType(ui_file)
    #     # self.ui = Form()
    #     #
    #     # self.ui.setupUi(self)
    #
    #     ui = uic.loadUi(ui_file)
        self.ui = uic.loadUi(ui_file, self)
    #
    #     #print(type(ui))
    #
    #     return ui
