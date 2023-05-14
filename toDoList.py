import sys
from functools import partial
from datetime import datetime as dt
from PySide6 import QtCore, QtGui
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow,
    QPushButton, QVBoxLayout, QWidget, QLineEdit, QListView, QGridLayout, QCalendarWidget, QDateTimeEdit, QCheckBox
)
import sqlite3
from sqlite3 import Error
import os
cwd = os.getcwd()
import random


conn = sqlite3.connect('bazka4.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS zadania
                 (nazwa TEXT, tresc TEXT, data TEXT, id INTEGER, czyWykonane INTEGER, czyWczasie INTEGER);''')
conn.commit()


class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.labelName = QLabel("Nazwa")
        self.inputName = QLineEdit()
        self.labelTask = QLabel("Podaj treść")
        self.inputTask = QLineEdit()
        self.calendar = QDateTimeEdit()
        self.calendar.setDateTime(QtCore.QDateTime.currentDateTime())
        self.addButton = QPushButton("Dodaj zadanie")
        self.addButton.clicked.connect(self.dodaj)
        layout.addWidget(self.labelName,0,0)
        layout.addWidget(self.inputName,0,1)
        layout.addWidget(self.labelTask,2,0)
        layout.addWidget(self.inputTask,2,1)
        layout.addWidget(self.calendar, 3, 0)
        layout.addWidget(self.addButton, 3, 1)
        self.setLayout(layout)

    def dodaj(self, checked):
        nazwa = self.inputName.text()
        tresc = self.inputTask.text()
        data = self.calendar.dateTime().toString(self.calendar.displayFormat())
        id = int(random.random() * 10 ** 9)

        c.execute("INSERT INTO zadania VALUES(?,?,?,?,?,?)",
                        (nazwa,tresc,data,id,0,3))
        conn.commit()

        w.aktualizuj()


class EditWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.idLabel = QLabel("cos")
        self.labelName = QLabel("Nazwa")
        self.inputName = QLineEdit()
        self.labelTask = QLabel("Podaj treść")
        self.inputTask = QLineEdit()
        self.calendar = QDateTimeEdit()
        self.calendar.setDateTime(QtCore.QDateTime.currentDateTime())
        self.addButton = QPushButton("Edytuj zadanie")
        self.addButton.clicked.connect(self.edytuj)
        layout.addWidget(self.labelName,0,0)
        layout.addWidget(self.inputName,0,1)
        layout.addWidget(self.labelTask,2,0)
        layout.addWidget(self.inputTask,2,1)
        layout.addWidget(self.calendar, 3, 0)
        layout.addWidget(self.addButton, 3, 1)
        self.setLayout(layout)




    def edytuj(self, checked):
        id = self.idLabel.text()
        nazwa = self.inputName.text()
        tresc = self.inputTask.text()
        data = self.calendar.dateTime().toString(self.calendar.displayFormat())

        firstDate = dt.strptime(data, "%d.%m.%Y %H:%M")
        secondDate = dt.strptime(QtCore.QDateTime.currentDateTime().toString(self.calendar.displayFormat()),
                                 "%d.%m.%Y %H:%M")
        toDbs = 1
        if (firstDate < secondDate):
            toDbs = 0


        c.execute("UPDATE zadania set nazwa=?, tresc=?, data=?,czyWczasie=? where id=?",
                        (nazwa,tresc,data,toDbs,id))
        conn.commit()

        w.aktualizuj()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.aktualizuj()


    def toggleWindow(self, checked):
        if self.window.isVisible():
            self.window.hide()
        else:
            self.window.show()
    def openEditWindow(self,nazwa,tresc,data,id):

        print(data, id)
        self.editWindow.inputName.setText(str(nazwa))
        self.editWindow.inputTask.setText(str(tresc))

        self.editWindow.idLabel.setText(str(id))
        # self.editWindow.calendar.setDateTime()
        if self.editWindow.isVisible():
            self.editWindow.hide()
        else:
            self.editWindow.show()
    def aktualizuj(self):
        # print("dasds")
        self.window = NewWindow()
        self.editWindow = EditWindow()

        self.layout = QGridLayout()
        self.button = QPushButton("Dodaj zadanie")
        self.button.clicked.connect(self.toggleWindow)
        self.layout.addWidget(self.button, 0, 0,1,7)

        sqlite_select_query = """SELECT * from zadania"""
        c.execute(sqlite_select_query)
        records = c.fetchall()

        i = 1

        for row in records:
            nazwa = QLabel(row[0])
            tresc = QLabel(row[1])
            data = QLabel(row[2])
            isdonelabel = QLabel("Niewykonane")

            name = row[0]
            text = row[1]
            date = row[2]
            id = row[3]
            isDone = row[4]
            intime = row[5]

            print(intime)

            if isDone == 1:
                isdonelabel = QLabel("Wykonane")


            firstDate = dt.strptime(date, "%d.%m.%Y %H:%M")
            secondDate = dt.strptime(QtCore.QDateTime.currentDateTime().toString(self.window.calendar.displayFormat()), "%d.%m.%Y %H:%M")

            # print(firstDate ,secondDate)
            if(intime==0 and isDone==1):
                color = QtGui.QColor(255, 0, 0)
                nazwa.setAutoFillBackground(True)  # This is important!!
                alpha = 140
                values = "{r}, {g}, {b}, {a}".format(r=color.red(),
                                                     g=color.green(),
                                                     b=color.blue(),
                                                     a=alpha
                                                     )
                nazwa.setStyleSheet("QLabel { background-color: rgba(" + values + "); }")
                tresc.setStyleSheet("QLabel { background-color: rgba(" + values + "); }")
                data.setStyleSheet("QLabel { background-color: rgba(" + values + "); }")
            elif(intime==1 and isDone==1):
                color = QtGui.QColor(0, 148, 12)
                nazwa.setAutoFillBackground(True)  # This is important!!
                alpha = 140
                values = "{r}, {g}, {b}, {a}".format(r=color.red(),
                                                     g=color.green(),
                                                     b=color.blue(),
                                                     a=alpha
                                                     )
                nazwa.setStyleSheet("QLabel { background-color: rgba(" + values + "); }")
                tresc.setStyleSheet("QLabel { background-color: rgba(" + values + "); }")
                data.setStyleSheet("QLabel { background-color: rgba(" + values + "); }")

            usun = QPushButton("usun")
            edytuj = QPushButton("edytuj")
            wykonaj = QPushButton("zmien status")



            usun.clicked.connect(lambda ignore=None,id=id: self.deleteRow(id))
            edytuj.clicked.connect(lambda ignore=None, name=name, text=text, date=date,id=id: self.openEditWindow(name,text,date,id))
            wykonaj.clicked.connect(lambda ignore=None,id=id,btn=wykonaj: self.changeCheck(id))

            self.layout.addWidget(nazwa, i, 0)
            self.layout.addWidget(tresc, i, 1)
            self.layout.addWidget(data, i, 2)
            self.layout.addWidget(usun, i, 3)
            self.layout.addWidget(edytuj, i, 4)
            self.layout.addWidget(isdonelabel, i, 5)
            self.layout.addWidget(wykonaj, i, 6)
            i += 1

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def deleteRow(self,id):
        # print(id)
        c.execute("DELETE FROM zadania WHERE id="+str(id))
        conn.commit()
        w.aktualizuj()

    def changeCheck(self,id):

        sqlite_select_query = "SELECT * from zadania where id="+str(id)
        c.execute(sqlite_select_query)
        records = c.fetchall()

        toDataBase = not records[0][4]

        if toDataBase == 0:
            c.execute("UPDATE zadania set czyWczasie=? where id=?",
                      (3, id))
            conn.commit()
        elif toDataBase == 1:
            firstDate = dt.strptime(records[0][2], "%d.%m.%Y %H:%M")
            secondDate = dt.strptime(QtCore.QDateTime.currentDateTime().toString(self.window.calendar.displayFormat()), "%d.%m.%Y %H:%M")
            if(firstDate<secondDate):
                c.execute("UPDATE zadania set czyWczasie=? where id=?",
                          (0, id))
                conn.commit()
            elif(firstDate>=secondDate):
                c.execute("UPDATE zadania set czyWczasie=? where id=?",
                          (1, id))
                conn.commit()

        c.execute("UPDATE zadania set czyWykonane=? where id=?",
                        (toDataBase,id))
        conn.commit()

        w.aktualizuj()



app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()