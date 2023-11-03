"""
    Главное окно АИС "ГСП Ремонт"
"""

import sys
import os

from PyQt6 import uic
from PyQt6 import QtWidgets, QtGui

from src.general_modules.resoursedir import DirUi, DirFont
from src.general_modules.resourseuser import AdminUser
from src.general_modules.connectDB import ConnectDb

from src.managementDB_modules.manager_gen_cmd import ManagerDBCmd


class AppMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_con = None
        self.con_db = None
        self.table_manager_cmd = None

        # Путь к файлу (элементу) интерфейса
        file_path = DirUi.MAIN_WINDOW.value

        # Загрузка файла (элемента) интерфейса
        uic.loadUi(os.path.join(*file_path), self)

        #   Подзаголовочное меню "Подключение"
        self.actBDcmda.triggered.connect(self.act_connectdb_cmd)  # Меню "Подключить БД КИПиА"
        self.actExit.triggered.connect(self.act_exit)             # Меню "Выход"

        #   Подзаголовочное меню "Редактирование БД"
        self.actGenCmd.triggered.connect(self.act_managerdb_cmd)    # Меню "Общие сведения о КИП"

    #   Обработчики меню "Подключение"
    # Меню "Подключить БД КИПиА"
    def act_connectdb_cmd(self):
        self.data_con = AdminUser.MAIN_AKK.value
        self.con_db = ConnectDb('gspcoast', *self.data_con)
        self.con_db.connect_db()

    # Меню "Выход"
    def act_exit(self):
        self.con_db.close_db()
        app.quit()

    #   Обработчики меню "Редактирование БД"
    #   Меню "Общие сведения о КИП"
    def act_managerdb_cmd(self):
        self.table_manager_cmd = ManagerDBCmd()




# Запуск Главного окна программы
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    #   Установка стиля отображения интерфейса
    app.setStyle('Fusion')

    #   Установка основного шрифта приложения
    font_path = DirFont.MAIN_FONT.value
    QtGui.QFontDatabase.addApplicationFont(os.path.join(*font_path))

    window = AppMain()
    window.showMaximized()
    window.show()
    sys.exit(app.exec())
