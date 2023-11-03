"""
    Модуль подключения к базе данных
"""
from PyQt6 import QtSql, QtWidgets


class ConnectDb(QtWidgets.QMessageBox):
    """Подключение к БД КИП и закрытие подключения"""
    def __init__(self, db_name, user_name, user_password):
        super().__init__()
        self.db_name = db_name
        self.user_name = user_name
        self.user_password = user_password
        self.msg_con = ''
        self.inf_con = None
        self.cmd_db = None

    #   Подключение (соединение) к БД КИП
    def connect_db(self):
        """Подключение к БД (PostgresSQL) с параметрами:
            - имя хоста (HostName);
            - наименование БД (DatabaseName);
            - имя пользователя (UserName);
            - пароль пользователя (Password)
           Вывод сообщения о состоянии подключения"""

        # Подключение к БД с параметрами
        self.cmd_db = QtSql.QSqlDatabase.addDatabase('QPSQL')
        self.cmd_db.setHostName('localhost')
        self.cmd_db.setDatabaseName(self.db_name)
        self.cmd_db.setUserName(self.user_name)
        self.cmd_db.setPassword(self.user_password)
        self.cmd_db.open()

        # Проверка состояния подключения
        if self.cmd_db.isOpen():
            self.msg_con = "Соединение с БД успешно"
        else:
            self.msg_con = "Соединение с БД не установлено"

        # Вывод сообщения о состоянии подключения
        self.inf_con = QtWidgets.QMessageBox.information(None,
                                                         'Соединение с базой данных',
                                                         self.msg_con,
                                                         buttons=QtWidgets.QMessageBox.StandardButton.Close,
                                                         defaultButton=QtWidgets.QMessageBox.StandardButton.Close)

    def close_db(self):
        """Закрытие подключения"""
        self.cmd_db.close()


