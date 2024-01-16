import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QApplication, QMainWindow, QTableWidget, QListView
from PyQt5 import QtWidgets, QtCore, QtGui
import Action
import random, string
import numpy as np
import sys
from math import radians

import robot_class
import robot_matplot

class AddActionForm(QtWidgets.QWidget):
    def __init__(self):
        super(AddActionForm, self).__init__()
        uic.loadUi('AddAction.ui', self)
        self.loadActions()
        self.show()

    def loadActions(self):
        # with open('Action.txt') as f:
        # data =  f.read()
        entries = ['Đứng', 'Ngồi', 'Giơ tay trái', 'Giơ tay phải', 'Giơ chân trái', 'Giơ chân phải']
        for i in entries:
            self.listWidgetActionBasic.addItem(i)
        

# nạp giao diện
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('UET_ARMUI.ui', self)

        # Thay đổi thành kết nối với sự kiện của nút trong UET_ARMUI.ui
        self.AddActionButton.clicked.connect(self.add_action_clicked)
        
        # define initial flag and value
        self.listActionName = set()
        self.listAction = dict()

        # self.ListActionView.itemDoubleClicked.connect(self._editJointPopup)
        # self.ListActionView.itemSelectionChanged.connect(self._countAction)

        #define view tab
        self.tabViewInitial()

        self.currentAction = 'Init'

        self.editName = None

        #define table view
        # self.endpoint.setColumnCount(3)
        self.endpoint.setHorizontalHeaderLabels(["X", "Y", "Z"])

        # define robot
        self.ur_change.toggled.connect(self.change_robot)
        
        self.change_robot()
        self.show()

    def add_action_clicked(self):
        # Hiển thị dialog AddAction khi nút "Add" được nhấn
        self.tempPopup = AddActionForm()
        self.tempPopup.btnSAVE.clicked.connect(self.save_button_clicked)

    def save_button_clicked(self):
        # Xử lý khi nút "Save" được nhấn
        tempNameSay = self.tempPopup.txtNameSay.toPlainText()
        tempNameMove = self.tempPopup.txtNameMove.toPlainText()
        if tempNameSay:
            self.ListActionView.addItem(self.tempPopup.txtNameSay.toPlainText() + ": " + self.tempPopup.txtSay.toPlainText())
            self.tempPopup.txtNameSay.clear()
            self.tempPopup.txtSay.clear()
        elif tempNameMove:
            self.ListActionView.addItem(self.tempPopup.txtNameMove.toPlainText() + ": " + self.tempPopup.txtX.toPlainText() + ', ' + self.tempPopup.txtY.toPlainText() + ', ' + self.tempPopup.txtZ.toPlainText())
            self.tempPopup.txtNameMove.clear()
            self.tempPopup.txtX.clear()
            self.tempPopup.txtY.clear()
            self.tempPopup.txtZ.clear()
        else:
            currentIndex = self.tempPopup.listWidgetActionBasic.currentRow()
            item = self.tempPopup.listWidgetActionBasic.item(currentIndex)
            self.ListActionView.addItem(item.text())
        # Đóng hộp thoại sau khi nhấn Save
        # self.tempPopup.close()

    def change_robot(self):
        #reset all first
            self.reset_all()
            if (self.ur_change.isChecked()): self.canvas.change_robot(robot_class.RobotUR5())

    def tabViewInitial(self):
            self.canvas = robot_matplot.DrawWidget()

            self.canvas.plot_done.connect(self.matlab_plot_done)
            self.canvas.plot_once.connect(self.update_endpointView)

            self.MatplotLayout.addWidget(self.canvas)

if __name__ == "__main__":
    # Tạo các đối tượng cho màn hình chính
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
