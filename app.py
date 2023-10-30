"""
    Главное окно АИС "ГСП Ремонт"
"""

import sys
import os

from PyQt6 import uic
from PyQt6 import QtWidgets, QtGui, QtSql

from src.general_modules.resoursedir import DirUi, DirFont
from src.general_modules.resourseuser import AdminUser
from src.general_modules.connectDB import DbCmd


class AppMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Путь к файлу (элементу) интерфейса
        self.con_db = None
        file_path = DirUi.MAIN_WINDOW.value

        # Загрузка файла (элемента) интерфейса
        uic.loadUi(os.path.join(*file_path), self)

        #   Подзаголовочное меню "Подключение"
        self.actBDcmda.triggered.connect(self.act_db_cmd)

    def act_db_cmd(self):
        data_con = AdminUser.MAIN_AKK.value
        con_db = DbCmd('gspcoast', *data_con)
        con_db.conn_cmd()











# Запуск Главного окна программы
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    #   Установка стиля отображения интерфейса
    app.setStyle('Fusion')

    #   Установка основного шрифта приложения
    font_path = DirFont.MAIN_FONT.value
    QtGui.QFontDatabase.addApplicationFont(os.path.join(*font_path))

    window = AppMain()
    window.show()
    sys.exit(app.exec())
