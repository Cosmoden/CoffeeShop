import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 1200, 1000)
        self.setWindowTitle('Кофе')
        uic.loadUi("main.ui", self)
        self.c = sqlite3.connect("coffee.sqlite3")
        self.pushButton.clicked.connect(self.add_type)
        self.pushButton_2.clicked.connect(self.edit_type)
        self.display()

    def display(self):
        cur = self.c.cursor()
        res = cur.execute(f"""SELECT * FROM coffee_types""").fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]))
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add_type(self):
        self.widget = AddEditWidget()
        self.widget.pushButton.clicked.connect(self.widget.add)
        self.widget.show()

    def edit_type(self):
        if len(self.tableWidget.selectedIndexes()) < 7:
            return
        self.widget = AddEditWidget()
        self.widget.pushButton.clicked.connect(self.widget.edit)
        self.widget.show()


class AddEditWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 400, 800, 600)
        self.setWindowTitle('Редактировать данные')
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.c = sqlite3.connect("coffee.sqlite3")
        self.spinBox.setRange(0, 1)
        self.spinBox_2.setRange(1, 5000)
        self.spinBox_3.setRange(10, 900)

    def add(self):
        cur = self.c.cursor()
        i = max([entry[0] for entry in cur.execute("""SELECT id FROM coffee_types""").fetchall()])
        cur.execute(f"""INSERT INTO coffee_types (id, name, roast_degree, ground, 
                                                    taste_desc, price, package_volume) 
                        VALUES ({i + 1}, '{self.lineEdit.text()}', '{self.lineEdit_2.text()}', 
                        {self.spinBox.value()}, '{self.textEdit.toPlainText()}', 
                        {self.spinBox_2.value()}, {self.spinBox_3.value()})""")
        self.c.commit()
        self.c.close()
        ex.display()

    def edit(self):
        cur = self.c.cursor()
        x = int(ex.tableWidget.selectedItems()[0].text())
        cur.execute(f"""UPDATE coffee_types 
                                SET name = '{self.lineEdit.text()}', roast_degree = '{self.lineEdit_2.text()}',
                                ground = {self.spinBox.value()}, taste_desc = '{self.textEdit.toPlainText()}',
                                price = {self.spinBox_2.value()}, package_volume = {self.spinBox_3.value()}
                                WHERE id = {x}""")
        self.c.commit()
        self.c.close()
        ex.display()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec())
