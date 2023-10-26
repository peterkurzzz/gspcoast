"""
    Главное окно АИС "Береговая"
"""

import sys
import os

from PyQt6 import uic
from PyQt6 import QtWidgets

from src.general_modules.resoursedir import DirUi


class AppMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        file_path = DirUi.MAIN_WINDOW.value         # Путь к файлу (элементу) интерфейса
        uic.loadUi(os.path.join(*file_path), self)  # Загрузка файла (элемента) интерфейса


# Запуск Главного окна программы
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AppMain()
    window.show()
    sys.exit(app.exec())
