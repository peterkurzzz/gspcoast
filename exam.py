"""
    Программа расчёта и анализа потребности в метрологическом
    обеспечении метрологических подразделений в составе РВО
"""

'''
    Подключение необходимых модулей
'''
import os.path
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSql

'''
    Подключение к базе исходных данных
'''


def connect_db():
    troops_db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    troops_db.setDatabaseName(r'si_troops.db')
    troops_db.open()
    if troops_db.isOpen():
        msgStatusBar = "Соединение с базой исходных данных успешно"
    else:
        msgStatusBar = "Соединение с базой исходных данных не установлено"
    return msgStatusBar


'''
    Формирование поискового запроса
'''


# def crt_query(*st, line_query):
#     query = ""
#     query = st[0] + " LIKE '%" + line_query + "%'"
#     if len(st) > 1:
#         for i in range(1, len(st)):
#             query = query + "  OR " + st[i] + " LIKE '%" + line_query + "%'"
#     return query


'''
    Кнопки редактирования БД
'''


#   Добавить запись
def add_record(x_model):
    x_row = x_model.rowCount()
    x_model.insertRow(x_row)


#   Удалить запись
def del_record(x_model, x_table):
    x_model.removeRow(x_table.currentIndex().row())


#   Сохранить БД
def save_table(x_model):
    x_model.submitAll()
    x_model.select()


def btn_reset_str():
    pass


'''
    Левая сторона отображения и редактирования списка (таблица)
'''


#    Таблица со списком

class DB_tableList(QtWidgets.QWidget):
    def __init__(self, ui_form, id_column: str, id_row=1):
        super().__init__()

        #    Переменные (параметры) таблицы
        self.table = None
        self.relation = None
        self.header = None
        self.delegate = None
        self.hide_col = None
        self.set_col = None

        #    Переменные модели
        self.table_List = None
        self.model_List = None
        self.arg_filter = None
        self.search_str = None
        self.query_filter = None

        #    Подключение графического интерфейса
        Form, Base = uic.loadUiType(os.path.join(".", "ui", ui_form))
        self.ui = Form()
        self.ui.setupUi(self)

        #    Переменные идентификаторов таблицы
        self.id_row = id_row
        self.id_column = id_column

        #    Построение таблицы списка

    def build_table(self,
                    table: str,
                    relation: dict,
                    header: dict,
                    delegate: int,
                    hide_col: list,
                    set_col: dict):
        self.table = table
        self.relation = relation
        self.header = header
        self.delegate = delegate
        self.hide_col = hide_col
        self.set_col = set_col

        #    Инициализация виджета
        self.table_List = self.ui.tableView_list

        #    Установление модели представления
        self.model_List = QtSql.QSqlRelationalTableModel()

        #    Установление модели редактирования
        self.model_List.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)

        #    Назначение таблицы БД в модель
        self.model_List.setTable(self.table)

        #    Установка связи с таблицами БД
        self.model_List.setRelation(
            self.relation['col'],
            QtSql.QSqlRelation(self.relation['rel_table'], self.relation['old_col'], self.relation['new_col']))

        #    Назначение заголовков модели
        for key in self.header.keys():
            self.model_List.setHeaderData(key, QtCore.Qt.Horizontal, self.header[key])

        #    Выбор модели и применение её для таблицы
        # self.model_List.setFilter("munit_name_cut = тбр")
        self.model_List.select()
        self.table_List.setModel(self.model_List)

        #    Установка делегата
        self.table_List.setItemDelegateForColumn(self.delegate, QtSql.QSqlRelationalDelegate(self.table_List))

        #    Определение скрываемых колонок
        for i in self.hide_col:
            self.table_List.hideColumn(i)

        #    Определение ширины отображаемых колонок
        for key in self.set_col.keys():
            self.table_List.setColumnWidth(key, self.set_col[key])

        #    Установка курсора на начало таблицы
        self.table_List.selectRow(self.id_row - 1)

        #   Сортировка по возрастанию и убыванию в столбце
        self.table_List.horizontalHeader().sectionClicked.connect(self.table_List.setSortingEnabled)

        #    Активация таблицы для выделения строк
        self.table_List.selectionModel().selectionChanged.connect(self.fnd_id)

    #    Определение ID выделенной строки
    def fnd_id(self):
        if self.table_List.selectionModel().currentIndex().isValid():
            # Выбираем значение ячейки
            self.id_row = self.model_List.data(
                self.model_List.index(self.table_List.selectionModel().currentIndex().row(),
                                      self.model_List.record().indexOf(self.id_column)))
        print(self.id_row)
        id_List = self.id_row

    #    Формирование критериев запроса для фильтрации
    def set_argFilter(self, arg_filter: list):
        self.arg_filter = arg_filter

    #    Добавление строки в таблицу
    def addRow_table(self):
        add_record(self.model_List)

    #    Удаление строки из таблицы
    def delRow_table(self):
        del_record(self.model.model_List, self.model.table_List)

    #    Сохранение изменений таблицы
    def saveRow_table(self):
        save_table(self.model.model_List)

    #    Фильтрация по строке поиска
    def filter_table(self, search_string):
        self.search_str = search_string
        self.query_filter = self.arg_filter[0] + " LIKE '%" + self.search_str + "%'"
        if len(self.arg_filter) > 1:
            for i in range(len(self.arg_filter)):
                self.query_filter += " OR " + self.arg_filter[i] + \
                                    " LIKE '%" + self.search_str + "%'"
        self.model_List.setFilter(self.query_filter)
        print(self.query_filter)


'''
   Блок кнопок управления таблицы левой стороны
'''


class DB_btnList(QtWidgets.QWidget):
    def __init__(self, ui_form, form_table):
        super().__init__()

        #    Переменные блока кнопок
        self.str_search = None
        self.form = form_table

        Form, Base = uic.loadUiType(os.path.join(".", "ui", ui_form))
        self.ui = Form()
        self.ui.setupUi(self)

        print(self.form.__dict__)

        #   Кнопки блока поиска
        self.ui.btnFind.clicked.connect(self.clk_search)
        self.ui.btnClear.clicked.connect(self.clk_search_clr)

        #   Кнопки редактирования таблицы
        self.ui.btnPlus.clicked.connect(self.form.addRow_table)
        self.ui.btnMinus.clicked.connect(self.form.delRow_table)
        self.ui.btnSave.clicked.connect(self.form.saveRow_table)

    #   Поиск по содержимому
    def clk_search(self):
        self.str_search = self.ui.strFind.text()
        self.form.filter_table(self.str_search)

    #   Сброс параметров поиска
    def clk_search_clr(self):
        self.ui.strFind.clear()
        self.str_search = ''
        self.form.filter_table(self.str_search)


'''
    Заголовок правой стороны
'''

class DB_titleStructure:
    def set_title(self):
        self.title = QtSql.QSqlQuery()
        self.title.prepare("SELECT munit_name "
                           "FROM m_unit "
                           "WHERE id_munit = (?)")
        self.title.addBindValue(self.id_List)
        self.title.exec_()
        self.title.next()
        self.textUn = self.title.value(self.title.record().indexOf('munit_name'))
        self.titleStr.setText(self.textUn)




'''
    Вкладка редактирования соединений
'''


class DBUnit(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Form, Base = uic.loadUiType(os.path.join(".", "ui", "DbUnit.ui"))
        self.ui = Form()
        self.ui.setupUi(self)

        #   Левая сторона (соединения)
        self.insert_list = self.ui.gridLayout_Left
        self.insert_list.setRowMinimumHeight(0, 641)

        #    Формирование таблицы (левая панель)
        self.table_List = DB_tableList(ui_form='DBTableList.ui', id_column='id_munit')
        self.table_List.build_table(
            table='m_unit',
            relation={'col': 3, 'rel_table': 'm_status', 'old_col': 'id_unit_status', 'new_col': 'unit_status'},
            header={1: 'Полное наименование', 2: 'Условное\nнаименование', 3: 'Статус'},
            delegate=3, hide_col=[0],
            set_col={1: 350, 2: 125, 3: 125}
        )
        self.table_List.set_argFilter(arg_filter=['munit_name', 'munit_name_cut', 'unit_status'])

        #    Отображение таблицы в левой панели
        self.insert_list.addWidget(self.table_List, 0, 0)

        #    Формирование блока кнопок (левая панель)
        self.table_List_btn = DB_btnList(ui_form='DBTableListBtn.ui', form_table=self.table_List)

        #    Отображение блока кнопок в левой панели
        self.insert_list.addWidget(self.table_List_btn, 1, 0)

        #   Правая сторона (соединения)
        self.insert_structure = self.ui.gridLayout_Right
        self.insert_structure.setRowMinimumHeight(0, 641)

        #   Формирование заголовка правой стороны
        self.title_structure = self.ui.nmUnit

    #     self.queryStr = '''
    #                     SELECT structure_munit.id_munit, structure_munit.id_div, m_division.div_name,
    #                     m_division.div_name_cut, m_status.unit_status, structure_munit.quan_div
    #                     FROM structure_munit, m_division, m_status
    #                     WHERE m_division.id_div = structure_munit.id_div
    #                     AND m_division.id_unit_status = m_status.id_unit_status
    #                     AND structure_munit.id_munit =
    #                     '''
    #     self.tblStr = self.ui.structureUnit
    #     self.sqmStr = QtSql.QSqlQueryModel()
    #     self.sqmStr.setQuery(self.queryStr + str(self.idUn))
    #     self.sqmStr.setHeaderData(2, QtCore.Qt.Horizontal, 'Полное наименование')
    #     self.sqmStr.setHeaderData(3, QtCore.Qt.Horizontal, 'Условное\nнаименование')
    #     self.sqmStr.setHeaderData(4, QtCore.Qt.Horizontal, 'Статус')
    #     self.sqmStr.setHeaderData(5, QtCore.Qt.Horizontal, 'Количество')
    #     self.tblStr.setModel(self.sqmStr)
    #     self.tblStr.hideColumn(0)
    #     self.tblStr.hideColumn(1)
    #     self.tblStr.setColumnWidth(2, 350)
    #     self.tblStr.setColumnWidth(3, 125)
    #     self.tblStr.setColumnWidth(4, 80)
    #     self.tblStr.setColumnWidth(5, 100)
    #
    #     #   Сортировка по возрастанию и убыванию в столбце
    #     self.tblUn.horizontalHeader().sectionClicked.connect(self.tblUn.setSortingEnabled)
    #
    #
    #
    #
    #
    #     #
    #     #   Формирование правой панели
    #     self.tblUn.selectionModel().selectionChanged.connect(lambda: self.clk_table(self.queryStr))
    #
    #       #  Редактировани правой панели !!!! потом открыть
    #       #  Поле выбора статуса подразделения
    #     self.comboSelDiv = self.ui.selStDiv
    #     self.querySDiv = QtSql.QSqlQuery()
    #     self.querySDiv.exec('SELECT unit_status FROM m_status')
    #     while self.querySDiv.next():
    #         self.comboSelDiv.addItem(self.querySDiv.value(self.querySDiv.record().indexOf('unit_status')))
    #     self.comboSelDiv.setEditText('')
    #     self.txtStDiv = ''
    #
    #     self.comboSelDiv.currentTextChanged.connect(self.sel_name_div)
    #
    #     #self.comboNmDiv.currentTextChanged.connect(self.sel_name_count_div)
    #
    # #  окно выбора наименования подразделения
    # def sel_name_div(self, s):
    #     self.txtStDiv = s
    #     self.comboNmDiv = self.ui.selNmDiv
    #     self.queryNmDiv = QtSql.QSqlQuery()
    #     self.comboNmDiv.setEnabled(True)
    #     self.queryNmDiv.prepare("SELECT m_division.div_name "
    #                             "FROM m_division, m_status "
    #                             "WHERE m_division.id_unit_status = m_status.id_unit_status "
    #                             "AND m_status.unit_status = (?)")
    #     self.queryNmDiv.addBindValue(self.txtStDiv)
    #     self.queryNmDiv.exec_()
    #     while self.queryNmDiv.next():
    #         self.comboNmDiv.addItem(self.queryNmDiv.value(self.queryNmDiv.record().indexOf('div_name')))
    #     self.comboNmDiv.setEditText('')
    #
    #     self.comboNmDiv.currentTextChanged.connect(self.sel_name_count_div)
    #
    # #  окно выбора краткого наименования и количества
    # def sel_name_count_div(self):
    #     print(self.comboNmDiv.currentText(), self.comboSelDiv.currentText())
    #     #    Запрос на формирование выборки для отображениея
    #     self.queryChDiv = QtSql.QSqlQuery()
    #     self.queryChDiv.prepare("SELECT m_division.id_div "
    #                             "FROM m_division, m_status "
    #                             "WHERE m_division.id_unit_status = m_status.id_unit_status "
    #                             "AND m_status.unit_status = (:stDiv) "
    #                             "AND m_division.div_name = (:nmDiv)")
    #     self.queryChDiv.bindValue(':stDiv', self.comboSelDiv.currentText())
    #     self.queryChDiv.bindValue(':nmDiv', self.comboNmDiv.currentText())
    #     self.queryChDiv.exec_()
    #     self.queryChDiv.next()
    #     self.idDiv = self.queryChDiv.value(self.queryChDiv.record().indexOf('id_div'))
    #
    #     self.sqmChDiv = QtSql.QSqlRelationalTableModel()
    #     self.sqmChDiv.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    #     self.sqmChDiv.setTable('structure_munit')
    #     self.sqmChDiv.setFilter('id_div = ' + str(self.idDiv) + ' AND id_munit = ' + str(self.idUn))
    #     #self.sqmChDiv.setRelation(1, QtSql.QSqlRelation('m_division', 'id_div', 'div_name_cut'))
    #     self.sqmChDiv.select()
    #
    #     self.mapperChDiv = QtWidgets.QDataWidgetMapper()
    #     self.mapperChDiv.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)
    #     self.mapperChDiv.setModel(self.sqmChDiv)
    #     self.mapperChDiv.addMapping(self.ui.nmDivCut, 1)
    #     self.mapperChDiv.addMapping(self.ui.setQuanDiv, 2)
    #     self.mapperChDiv.toFirst()
    #

    #
    # #   Правая таблица (состав - подразделения)
    # def clk_table(self, x_query):
    #     if self.tblUn.currentIndex().isValid():
    #         # Выбираем значение ячейки
    #         self.idUn = self.sqmUn.data(
    #             self.sqmUn.index(self.tblUn.currentIndex().row(),
    #                              self.sqmUn.record().indexOf('id_munit')))
    #
    #         queryStr_isp = x_query + str(self.idUn)
    #         self.sqmStr.setQuery(queryStr_isp)
    #         self.tblStr.setModel(self.sqmStr)
    #
    #         #   Смена заголовка
    #         self.title.addBindValue(self.idUn)
    #         if self.title.exec_():
    #             while self.title.next():
    #                 self.textUn = self.title.value(self.title.record().indexOf('munit_name'))
    #         self.titleStr.setText(self.textUn)
    #     else:
    #         pass
    #


'''
    Окно редактирования списка статусов
'''


class _DBStatus(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        Form, Base = uic.loadUiType(os.path.join(".", "ui", "DbStatWin.ui"))
        self.ui = Form()
        self.ui.setupUi(self)

        self.tbl = self.ui.tabStat
        self.sqm = QtSql.QSqlTableModel()
        self.sqm.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.sqm.setTable('m_status')
        self.sqm.setHeaderData(1, QtCore.Qt.Horizontal, 'Перечень статусов')
        self.sqm.select()
        self.tbl.setModel(self.sqm)
        self.tbl.hideColumn(0)
        self.tbl.setColumnWidth(1, 200)
        self.tbl.selectRow(0)

        #   Сортировка по возрастанию и убыванию в столбце
        self.tbl.horizontalHeader().sectionClicked.connect(self.tbl.setSortingEnabled)

        #   Кнопки управления
        self.ui.btnPlus.clicked.connect(lambda: add_record(self.sqm))
        self.ui.btnMinus.clicked.connect(lambda: del_record(self.sqm, self.tbl))
        self.ui.btnSave.clicked.connect(lambda: save_table(self.sqm))
        self.ui.btnClose.clicked.connect(lambda: self.close())


'''
    Главное меню   
'''


class MainWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        Form, Base = uic.loadUiType(os.path.join(".", "ui", "MainWin.ui"))
        self.ui = Form()
        self.ui.setupUi(self)
        connect_db()
        # statusbar = self.ui.tabWidget
        # statusBar = self.ui.statusbar.showMessage(connect_db(), 10000)
        # statusBar.showMessage(msgStatusBar, 10000)

        #   Подзаголовочное меню
        self.ui.actStat.triggered.connect(self.clk_status)
        self.ui.actExit.triggered.connect(QtWidgets.qApp.quit)
        self.ui.actUnitBd.triggered.connect(self.show_tab_unit)

        #   Кнопки управления основного меню
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.btnQuitMain.clicked.connect(QtWidgets.qApp.quit)

    # Открыть вкадку правки БД соединений
    def show_tab_unit(self):
        self.DbUn = DBUnit()
        self.ui.tabWidget.addTab(self.DbUn, 'Соединения и отдельные воинские части')
        index_win = self.ui.tabWidget.indexOf(self.DbUn)

    #   Дополнительные списки
    #       Редактирование списка статусов
    def clk_status(self):
        self.dbStat = _DBStatus()
        self.dbStat.show()

    #   Закрыть вкладку
    def close_tab(self, index_win):
        self.ui.tabWidget.removeTab(index_win)


'''
    Тело программы
'''

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    QtGui.QFontDatabase.addApplicationFont(os.path.join(".", "font", "PT-Astra-Serif_Regular.ttf"))

    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec_())