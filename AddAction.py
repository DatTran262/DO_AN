import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QApplication, QMainWindow, QTableWidget, QListView
from PyQt5 import QtWidgets, QtCore, QtGui

class AddActionForm(QtWidgets.QWidget):
    def __init__(self):
        super(AddActionForm, self).__init__()
        uic.loadUi('AddAction.ui', self)

        # Kết nối sự kiện nhấn nút "Save" với hàm xử lý
        self.btnSAVE.clicked.connect(self.save_button_clicked)

    def save_button_clicked(self):
        # Xử lý khi nút "Save" được nhấn
        name = self.say_name_edit.toPlainText()
        dialog = self.say_dialog_edit.toPlainText()
        print(f'Save Clicked for Say: Name={name}, Dialog={dialog}')
