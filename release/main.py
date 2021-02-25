import sys

from PyQt5 import uic  # Импортируем uic 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import addEditCoffeeForm

class Example(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI\main.ui", self)
        self.con = sqlite3.connect("data\coffee.db")
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.up)
    
    def update_result(self):
        self.con = sqlite3.connect("data\coffee.db")
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute(f"""SELECT * FROM coffe WHERE (id > 0)""").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        self.tableWidget.setColumnCount(len(result[0]))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def up(self):
        self.update_result()  
                
    def add(self, text):
        self.colr = [i[0] for i in self.con.cursor().execute(f"""SELECT id FROM coffe WHERE (id > 0)""").fetchall()][-1]
        self.second_form = SecondForm(self.colr)
        self.second_form.show()        
        
        
class SecondForm(QWidget):
    def __init__(self, col):
        super().__init__()
        addEditCoffeeForm.Ui_Form.setupUi(self)
        # uic.loadUi("addEditCoffeeForm.ui", self)
        self.pushButton.clicked.connect(self.add)
        self.title = ''
        self.step = ''
        self.podacha = 'Молотый'
        self.opis = ''
        self.chena = 0
        self.obem = 0
        self.col = col
        print(col)
        self.con = sqlite3.connect("data\coffee.db")
        cur = self.con.cursor()
        self.comboBox.activated[str].connect(self.onActivated)
    
    def onActivated(self, text):
        self.podacha = text
    
    def add(self):
        if (self.lineEdit.text() == '') or (self.lineEdit_2.text() == '') or (self.lineEdit_3.text() == '') or \
                (not self.lineEdit_4.text().isdigit()) or (not self.lineEdit_5.text().isdigit()):
            self.label_5.setText('Неверно заполненая форма')

        else:
            self.title = self.lineEdit.text()
            self.step = self.lineEdit_2.text()
            self.opis = self.lineEdit_3.text()
            self.chena = self.lineEdit_4.text()
            self.obem = self.lineEdit_5.text()
            cur = self.con.cursor()
            cur.execute(f"""INSERT INTO coffe
                          (ID, name, roastring, Ground, Description, price, volume)
                          VALUES
                            ({int(self.col + 1)}, '{str(self.title)}', '{str(self.step)}', '{str(self.podacha)}', 
                            '{str(self.opis)}', '{int(self.chena)}', '{self.obem}');""")
            self.con.commit()
            self.con.close()
            self.close()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())