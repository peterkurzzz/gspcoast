"""
    Модуль-конструктор таблиц представления данных БД
"""

import os

from PyQt6 import uic
from PyQt6 import QtWidgets, QtSql, QtCore


class BuilderTab(QtWidgets.QWidget):
    """Конструктор таблиц данных БД по параметрам:
        - """
    def __init__(self, ui_form: object, id_column: str, id_row=1):
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

        # #    Подключение графического интерфейса
        # Form, Base = uic.loadUiType(os.path.join(".", "ui", ui_form))
        # self.ui = Form()
        # self.ui.setupUi(self)

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