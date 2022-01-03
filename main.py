import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from random import *
import sqlite3


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Кофе')
        uic.loadUi("main.ui", self)
        self.c = sqlite3.connect("coffee.sqlite3")
        self.display()

    def display(self):
        cur = self.c.cursor()
        res = cur.execute(f"""SELECT * FROM coffee_types""").fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]))
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
