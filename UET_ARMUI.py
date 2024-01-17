import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QApplication, QMainWindow, QTableWidget, QListView
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

        # define signal and slot
        self.AddActionButton.clicked.connect(self.add_action_clicked)
        self.DeleteActionButton.clicked.connect(self.openDelPopup)
        self.EditActionButton.clicked.connect(self.editJointPopup)
        # self.PoseActionButton.clicked.connect(self.openPoseTab)
        self.ExecuteActionButton.clicked.connect(self.pre_execute)
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

    def matlab_plot_done(self):
        if (self.ExecuteActionButton.text() == "Pause"):
            self.ExecuteActionButton.setText("Execute")

    def update_endpointView(self):
        self.endpoint.insertRow(self.endpoint.rowCount())
        self.endpoint.setItem(self.endpoint.rowCount()-1, 0, QtWidgets.QTableWidgetItem( "{:.5f}".format(self.canvas.robot.waypointX[-1] )))
        self.endpoint.setItem(self.endpoint.rowCount()-1, 1, QtWidgets.QTableWidgetItem( "{:.5f}".format(self.canvas.robot.waypointY[-1] )))
        self.endpoint.setItem(self.endpoint.rowCount()-1, 2, QtWidgets.QTableWidgetItem( "{:.5f}".format(self.canvas.robot.waypointZ[-1] )))

        self.endpoint.scrollToBottom()

    def reset_all(self):
        self.endpoint.clearContents()
        self.endpoint.setRowCount(0)

        if (self.ExecuteActionButton.text() == "Pause"):
            self.canvas.plot_pause()
            self.ExecuteActionButton.setText("Execute")

        self.listActionName = set()
        self.listAction = dict()

        self.currentAction = 'Init'
        self.editName = None

    def openDelPopup(self):
        currentSelected = self.ListActionView.selectedItems()
        if not currentSelected: return        

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Confirm Deleting " + str(len(currentSelected)) +" Item ?")
        msgBox.setWindowTitle("Warning Box")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            for item in currentSelected:
                del_item = self.ListActionView.takeItem(self.ListActionView.row(item))
                q_action_name = del_item.text()
                try:
                    self.listAction.pop(q_action_name)
                    self.listActionName.remove(q_action_name)
                except:
                    pass

    def editJointPopup(self):
        currentSelected = self.ListActionView.selectedItems()
        if not currentSelected: return 
        self._editJointPopup(currentSelected[-1])

    def _editJointPopup(self, last_item):
        last_item_id = self.ListActionView.row(last_item)
        self.editName = None
        if (self.listAction.get(last_item.text()) is None): return
        self.editName = last_item.text()

        self.tempPopup = ActionPopup()
        self.tempPopup.ActionthLabel.setText(str("Action: "+str(last_item_id)))
        self.tempPopup.JointhValue.setMaximum ( self.canvas.robot.numJoint - 1 )
        self.tempPopup.JointhValue.valueChanged.connect( self.adaptJointID )
    
        self.coverPopup(self.listAction[self.editName])
        self.currentAction = 'Edit'
        self.tempPopup.ActionNameLabel.setReadOnly(True)
        self.tempPopup.ActionButton.clicked.connect(self.saveAction)
        self.tempPopup.exec()

    def pre_execute(self):
        if (self.ExecuteActionButton.text() == "Execute"):

            self.endpoint.clearContents()
            self.endpoint.setRowCount(0)

            self.execute()
            # self.CurrentTotalTimeValue.setText(str( len(self.canvas.jointTrajectory) ))
            self.canvas.robot_limit_plot()
            self.ExecuteActionButton.setText("Pause")
        elif (self.ExecuteActionButton.text() == "Pause"):
            self.canvas.plot_pause()
            self.ExecuteActionButton.setText("Execute")

    def execute(self):
        POSE_TYPE = 808
        JOINT_TYPE = 404

        currentSelected = self.ListActionView.selectedItems()
        if not currentSelected: 
            self.canvas.setJointTrajectory(None)
            return

        tempDict = {}
        for item in currentSelected:
            tempDict[self.ListActionView.row(item)] = item
        tempIndexes = sorted(tempDict)

        # define a list to contain the resultant items i.e sorted items
        tempGroup = []
        for index in tempIndexes:
            if tempDict[index].type() == POSE_TYPE:
                tempGroup.append(self.canvas.List_Pose[tempDict[index].text() ])
            else:
                tempGroup.append(self.listAction[ tempDict[index].text() ])


        timeTable = robot_class.TimeTable(self.canvas.robot.numJoint, self.canvas.robot.QHome)
        timeTable.prepare(tempGroup)
        self.canvas.setJointTrajectory(timeTable.gen_jointList())

if __name__ == "__main__":
    # Tạo các đối tượng cho màn hình chính
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
