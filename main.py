# необходимые библиотеки
import os
import sys
import csv
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *


# СОЗДАЕМ ГЛАВНЫЙ КЛАСС "ОКНА" ПРИЛОЖЕНИЯ
class MainWindow(QMainWindow):

    # конструктор
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # размеры окна
        self.setGeometry(100, 100, 600, 400)

        # создаем слои
        layout = QVBoxLayout()

        # создаем QPlainTextEdit object
        self.editor = QPlainTextEdit()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['Логи (записи)'])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.buttonSave = QPushButton('Записать в журнал (логи)', self)
        self.buttonSave.clicked.connect(self.handle_save)

        self.buttonOpen = QPushButton('Открыть журнал (логи)', self)
        self.buttonOpen.clicked.connect(self.handle_open)

        self.buttonCl = QPushButton('Удалить запись (лог), файл', self)
        self.buttonCl.clicked.connect(self.button_cl)

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        self.path = None

        # добавление элементов на слой
        layout.addWidget(self.editor)

        layout.addWidget(self.tableWidget)

        layout.addWidget(self.buttonSave)

        layout.addWidget(self.buttonOpen)

        layout.addWidget(self.buttonCl)

        # создаем QWidget layout
        container = QWidget()

        # установка слоя в контайнер
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.status = QStatusBar()

        self.setStatusBar(self.status)

        file_toolbar = QToolBar("File")

        self.addToolBar(file_toolbar)

        # creating a file menu
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction("Open file", self)

        open_file_action.setStatusTip("Open file")

        open_file_action.triggered.connect(self.file_open)

        file_menu.addAction(open_file_action)

        file_toolbar.addAction(open_file_action)

        save_file_action = QAction("Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction("Save As", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction("Print", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")

        self.addToolBar(edit_toolbar)

        edit_menu = self.menuBar().addMenu("&Edit")


        undo_action = QAction("Undo", self)

        undo_action.setStatusTip("Undo last change")

        undo_action.triggered.connect(self.editor.undo)

        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setStatusTip("Redo last change")

        redo_action.triggered.connect(self.editor.redo)

        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        cut_action = QAction("Cut", self)
        cut_action.setStatusTip("Cut selected text")

        cut_action.triggered.connect(self.editor.cut)

        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setStatusTip("Copy selected text")

        copy_action.triggered.connect(self.editor.copy)

        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setStatusTip("Paste from clipboard")

        paste_action.triggered.connect(self.editor.paste)

        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction("Select all", self)
        select_action.setStatusTip("Select all text")

        select_action.triggered.connect(self.editor.selectAll)

        edit_toolbar.addAction(select_action)
        edit_menu.addAction(select_action)

        wrap_action = QAction("Wrap text to window", self)
        wrap_action.setStatusTip("Check to wrap text to window")

        wrap_action.setCheckable(True)

        wrap_action.setChecked(True)

        wrap_action.triggered.connect(self.edit_toggle_wrap)

        edit_menu.addAction(wrap_action)

        self.update_title()

        self.show()

    def dialog_critical(self, s):

        dlg = QMessageBox(self)

        dlg.setText(s)

        dlg.setIcon(QMessageBox.Critical)

        dlg.show()

    # действия при открытии файла (записки)
    def file_open(self):

        path, _ = QFileDialog.getOpenFileName(self, "Open file", "","csv (*.csv)")

        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()

            # if some error occurred
            except Exception as e:

                self.dialog_critical(str(e))
            # else
            else:
                # обновление пути к файлу
                self.path = path

                # обновление текста
                self.editor.setPlainText(text)

                self.update_title()

    def file_save(self):

        if self.path is None:
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):

        # открытие по пути
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", ".csv (*.csv)")

        if not path:

            return

        self._save_to_path(path)

    # сохранение с путем к файлу
    def _save_to_path(self, path):

        current_datetime = datetime.datetime.now()
        str_date = current_datetime.strftime("%d-%m-%Y %H:%M")

        text = self.editor.toPlainText()
        data = [(str_date, text)]
        nr = self.tableWidget.rowCount()
        self.tableWidget.insertRow(nr)
        self.tableWidget.setItem(nr, 0, QTableWidgetItem(path))

        # try catch блок
        try:

            # открытия файла для записи
            with open(path, 'w', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(data)

        except Exception as e:

            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    # действия призапуске диалога печати
    def file_print(self):

        # диалог распечатки
        dlg = QPrintDialog()

        # при запуске
        if dlg.exec_():
            # print the text
            self.editor.print_(dlg.printer())

    # обновление названия (заголовка приложения)
    def update_title(self):

        # суффикс - название сохраненого файла
        self.setWindowTitle("%s - Записная книжка (Записки. Notes)" % (os.path.basename(self.path)
                                                    if self.path else "Без названия"))

    def edit_toggle_wrap(self):

        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)

    def handle_save(self):
        try:

            with open('log33.csv', 'w', encoding='utf-8') as file2:
                writer = csv.writer(file2)
                rowdata = []
                for row in range(self.tableWidget.rowCount()):

                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            rowdata.append(item.text())
                        else:
                            rowdata.append('')
                            #return
                    writer.writerow(rowdata)
                    rowdata = []
        except Exception as e:
            # show error using critical
            self.dialog_critical(str(e))

    def handle_open(self):
        try:

            with open('log33.csv', 'r') as file:
                    # использование reader для чтения файла
                reader = csv.reader(file)

                for row in reader:
                        # Добавить строку (запись) в таблицу
                    if len(row) == 0:
                        continue
                    row_index = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_index)
                        # встасить данные в ячейку
                    for col_index, cell in enumerate(row):
                        if os.path.isfile(cell):
                            self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(cell))
        except Exception as e:
            # показать ошибки
            self.dialog_critical(str(e))

    def button_cl(self):
        row = self.tableWidget.currentRow()
        column = self.tableWidget.currentColumn()
        item = self.tableWidget.itemAt(row, column)
        if os.path.isfile(item.text()):
            os.remove(item.text())
        if row > -1:  # Если есть выделенная строка/элемент
            self.tableWidget.removeRow(row)
            # Следующий вызов нужен для того, чтобы
            # сбросить индекс выбранной строки (чтобы currentRow установился в -1)
            self.tableWidget.selectionModel().clearCurrentIndex()

# код "запуска"
if __name__ == '__main__':
    # создаем PyQt5 приложение
    app = QApplication(sys.argv)

    # устанавливаем имя приложения
    app.setApplicationName("PyQt5-Note")

    # создаем главное окно приложения
    window = MainWindow()

    # цикл
    app.exec_()
