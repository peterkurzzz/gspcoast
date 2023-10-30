"""
    Модуль подключения к базе данных
"""
from PyQt6 import QtSql, QtWidgets


class DbCmd(QtWidgets.QMessageBox):
    def __init__(self, db_name, user_name, user_password):
        super().__init__()
        self.db_name = db_name
        self.user_name = user_name
        self.user_password = user_password
        self.msg_con = ''
        self.inf_con = None

    def conn_cmd(self):
        cmd_db = QtSql.QSqlDatabase.addDatabase('QPSQL')
        cmd_db.setHostName('localhost')
        cmd_db.setDatabaseName(self.db_name)
        cmd_db.setUserName(self.user_name)
        cmd_db.setPassword(self.user_password)
        cmd_db.open()
        if cmd_db.isOpen():
            self.msg_con = "Соединение с базой исходных данных успешно"
        else:
            self.msg_con = "Соединение с базой исходных данных не установлено"

        self.inf_con = QtWidgets.QMessageBox.information(None, 'Соединение с базой данных', self.msg_con,
                                                         buttons=QtWidgets.QMessageBox.StandardButton.Close,
                                                         defaultButton=QtWidgets.QMessageBox.StandardButton.Close)
        #self.inf_con.show()

