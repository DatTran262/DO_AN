import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QApplication, QMainWindow, QTableWidget, QListView, QCheckBox
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QPoint
import Action
import random, string
import numpy as np
import sys
from math import radians
import math

import robot_class
import robot_matplot

entries = []
entries_dict = {}

listAction = dict()
listActionName = []
listActionNameOrigin = []

listLockName = ['All', 'Foot', 'Left hand', 'Right hand']
listLock = dict()

listZip = dict()
listZipName = set()

def load_presetAction():
        file_path = "Action.txt"

        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():
                    entrie, *other_values = line.strip().split()
                    entries.append(entrie)
                    entries_dict[entrie] = robot_class.JointAction(entrie, int(other_values[0]), float(other_values[1]), float(other_values[2]))
load_presetAction()

def creatListAction():
    for entry in entries: 
        entry_name = entry
        if entry_name not in listActionNameOrigin:
            listActionNameOrigin.append(entry_name)     
        listAction[entry_name] = entries_dict[entry]
creatListAction()

class AddActionForm(QtWidgets.QWidget):

    def __init__(self):
        super(AddActionForm, self).__init__()
        uic.loadUi('AddAction.ui', self)

        self.loadActions()

        self.show()

    def loadActions(self):

        for i in listActionNameOrigin:
            self.listWidgetActionBasic.addItem(i)

class ActionPopup(QtWidgets.QDialog):
    def __init__(self):
        super(ActionPopup, self).__init__() 
        uic.loadUi('JointPopup.ui', self) 
        self.show() 

class AddZip(QtWidgets.QDialog):

    def __init__(self):
        super(AddZip, self).__init__()
        uic.loadUi('Zip.ui', self)
        self.show()
        
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
        self.timer = QTimer()

        #define view tab
        self.tabViewInitial()

        self.currentAction = 'Init'

        self.editName = None

        #define table view
        # self.endpoint.setColumnCount(3)
        self.endpoint.setHorizontalHeaderLabels(["X", "Y", "Z"])

        # define robot
        # self.ur_change.toggled.connect(self.change_robot)
        self.change_robot()
        self.show()

    def save_button_clicked(self):
        # Xử lý khi nút "Save" được nhấn
        tempNameSay = self.tempPopup.txtNameSay.toPlainText()
# need better handle here, but maybe for now is NOT okay
        if self.tempPopup.tabWidgetAction.tabText(self.tempPopup.tabWidgetAction.currentIndex()) == 'Say': 
            currentName = self.tempPopup.txtNameSay.toPlainText()
            if currentName in listActionNameOrigin:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("Tên đã tồn tại trong danh sách.")
                msgBox.setWindowTitle("Warning Box")

                returnValue = msgBox.exec()
                self.tempPopup.txtNameMove.clear()

            else:
                self.ListActionView.addItem(currentName + ": " + self.tempPopup.txtSay.toPlainText())

                self.tempPopup.txtNameSay.clear()
                self.tempPopup.txtSay.clear()
        elif self.tempPopup.tabWidgetAction.tabText(self.tempPopup.tabWidgetAction.currentIndex()) == 'Joint Action':
            currentIndex = self.tempPopup.listWidgetActionBasic.currentRow()
            item = self.tempPopup.listWidgetActionBasic.item(currentIndex)
            currentName = item.text()
            self.ListActionView.addItem(QtWidgets.QListWidgetItem(currentName, type = 404))
        else:
            if self.tempPopup.checkBoxFJ.isChecked():
                count = self.ListActionView.count()
                id_follow = listAction[self.ListActionView.item(count-1).text()].jointID
                print('id:', id_follow)
                self.ListActionView.addItem(QtWidgets.QListWidgetItem(str('Follow joint'), type = 101))
                listLock['Follow joint'] = robot_class.Lock(['Follow joint'], id_follow)
            else:            
                temp_part = []
                if self.tempPopup.checkBoxALL.isChecked(): temp_part.append('A')
                if self.tempPopup.checkBoxF.isChecked(): temp_part.append('F')
                if self.tempPopup.checkBoxHL.isChecked(): temp_part.append('L')
                if self.tempPopup.checkBoxHR.isChecked(): temp_part.append('R')
                if self.tempPopup.checkBoxH_6.isChecked(): temp_part.append('6')
                if self.tempPopup.checkBoxH_7.isChecked(): temp_part.append('7')
                if self.tempPopup.checkBoxH_8.isChecked(): temp_part.append('8')
                if self.tempPopup.checkBoxH_9.isChecked(): temp_part.append('9')
                if self.tempPopup.checkBoxH_10.isChecked(): temp_part.append('10')
                if self.tempPopup.checkBoxH_11.isChecked(): temp_part.append('11')

                str_part = 'P_Lock '
                for i in temp_part: str_part = str_part + i + ' '

                self.ListActionView.addItem(QtWidgets.QListWidgetItem(str_part, type = 101))
                listLock[str_part] = robot_class.Lock(temp_part, 0)

        # check_plock()
        
        # self.tempPopup.close()

    def add_action_clicked(self):

        entries.clear()
        entries_dict.clear()
        load_presetAction()

        # Hiển thị dialog AddAction khi nút "Add" được nhấn
        self.tempPopup = AddActionForm()

# Load file
        creatListAction()
        listActionName = listActionNameOrigin.copy()
        # print('listAction:', listAction)
        print('listActionName:', listActionName)
        print('listActionNameOrigin:', listActionNameOrigin)

        self.tempPopup.btnSAVE.clicked.connect(self.save_button_clicked)
        self.tempPopup.btnJointAction.clicked.connect(self.openAddPopup)
        self.tempPopup.btnZip.clicked.connect(self.openAddZip)

        self.tempPopup.AddPoseButton.clicked.connect(self.addPosePopup)
        self.tempPopup.NewPoseButton.clicked.connect(self.setPose)
        # self.tempPopup.exec()

    def change_robot(self):
        #reset all first
            self.reset_all()
            self.canvas.change_robot(robot_class.RobotUR5())
            # if (self.ur_change.isChecked()): self.canvas.change_robot(robot_class.RobotUR5())

    def tabViewInitial(self):
            self.canvas = robot_matplot.DrawWidget()

            self.canvas.plot_done.connect(self.matlab_plot_done)
            self.canvas.plot_once.connect(self.update_endpointView)

            self.MatplotLayout.addWidget(self.canvas)

    def matlab_plot_done(self):
        if (self.ExecuteActionButton.text() == "Pause"):
            self.ExecuteActionButton.setText("Execute")

    #
    def update_endpointView(self): # in ra điểm base với tọa độ X, Y, speed cua robot
        self.endpoint.insertRow(self.endpoint.rowCount())
        self.endpoint.setItem(self.endpoint.rowCount()-1, 0, QtWidgets.QTableWidgetItem( "{:.5f}".format(self.canvas.robot.waypointX[1] )))
        self.endpoint.setItem(self.endpoint.rowCount()-1, 1, QtWidgets.QTableWidgetItem( "{:.5f}".format(self.canvas.robot.waypointY[1] )))
        self.endpoint.setItem(self.endpoint.rowCount()-1, 2, QtWidgets.QTableWidgetItem( "{:.5f}".format(self.canvas.robot.jointSpeeds[1] )))

        self.endpoint.scrollToBottom()

    def addPosePopup(self):
        item, ok = QtWidgets.QInputDialog.getItem(self, 'Pose Dialog', 'Select pose', list(self.canvas.List_Pose.keys()), 0, False)
        # item la string chua ten cua Pose
        if ok and item:
            newItem = QtWidgets.QListWidgetItem(item, type = 808)
            newItem.setIcon(QtGui.QIcon("pose.jpg"))
            self.ListActionView.addItem(newItem)

    # need to write manual
    def setPose(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Pose Name Input Dialog', 'Enter pose name:')
        if (ok):
            if (text == 'Home'):
                self.canvas.robot.QHome = robot_class.Pose(text, self.canvas.robot.Q.copy(), self.canvas.robot.poseJointSpeeds)
              
            self.canvas.List_Pose[text] = robot_class.Pose(text, self.canvas.robot.Q.copy(), self.canvas.robot.poseJointSpeeds)
# hiển thị các cửa sổ nhỏ của AddAction
    def openAddPopup(self):
        self.tempPopup.temmpPopup = ActionPopup()
        self.tempPopup.temmpPopup.ActionthLabel.setText(str("Action: "+str(self.ListActionView.count())))
        self.tempPopup.temmpPopup.ActionNameLabel.setText( ''.join(random.choices(string.ascii_uppercase + string.digits, k=1 + self.ListActionView.count())) )
        self.tempPopup.temmpPopup.SpeedValue.setValue( self.canvas.robot.jointSpeeds[0] )
        self.tempPopup.temmpPopup.JointhValue.setMaximum ( self.canvas.robot.numJoint - 1 )
        self.adaptJointID()
        self.tempPopup.temmpPopup.JointhValue.valueChanged.connect( self.adaptJointID )
        self.currentAction = 'Add'

        self.tempPopup.temmpPopup.ActionButton.clicked.connect(self.saveAction)
        self.tempPopup.temmpPopup.exec()

    def adaptJointID(self):
        jID =  self.tempPopup.temmpPopup.JointhValue.value()
        if (self.currentAction == 'Add'): self.tempPopup.temmpPopup.SpeedValue.setValue(  self.canvas.robot.jointSpeeds[ jID ] )
        self.tempPopup.temmpPopup.JointhTargetValue.setMaximum(self.canvas.robot.limit[jID][1] - 0.0001)
        self.tempPopup.temmpPopup.JointhTargetValue.setMinimum(self.canvas.robot.limit[jID][0] + 0.0001)

        if ( self.canvas.robot.jointType[ jID ] == 'r' ):
            self.tempPopup.temmpPopup.RevoluteRadioButton.setChecked(1)
            self.tempPopup.temmpPopup.SpeedValue.setSuffix(" rad")
            self.tempPopup.temmpPopup.JointhTargetValue.setSuffix(" rad")
        else:
            self.tempPopup.temmpPopup.PrismaticRadioButton.setChecked(1)
            self.tempPopup.temmpPopup.SpeedValue.setSuffix(" m")
            self.tempPopup.temmpPopup.JointhTargetValue.setSuffix(" m")

    def coverPopup(self, jointAction):
        self.tempPopup.temmpPopup.ActionNameLabel.setText( jointAction.name )
        self.tempPopup.temmpPopup.JointhValue.setValue(jointAction.jointID)
        self.adaptJointID()
        self.tempPopup.temmpPopup.SpeedValue.setValue( jointAction.speed )
        self.tempPopup.temmpPopup.JointhTargetValue.setValue( jointAction.targetValue )

    def reset_all(self):
        self.endpoint.clearContents()
        self.endpoint.setRowCount(0)

        if (self.ExecuteActionButton.text() == "Pause"):
            self.canvas.plot_pause()
            self.ExecuteActionButton.setText("Execute")

        listActionName = []

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
                    listAction.pop(q_action_name)
                    listActionName.remove(q_action_name)
                except:
                    pass

    def editJointPopup(self):
        currentSelected = self.ListActionView.selectedItems()
        if not currentSelected: return 
        self._editJointPopup(currentSelected[-1])

    def _editJointPopup(self, last_item):
        last_item_id = self.ListActionView.row(last_item)
        self.editName = None
        if (listAction.get(last_item.text()) is None): return
        self.editName = last_item.text()

        self.tempPopup.temmpPopup = ActionPopup()
        self.tempPopup.temmpPopup.ActionthLabel.setText(str("Action: "+str(last_item_id)))
        self.tempPopup.temmpPopup.JointhValue.setMaximum ( self.canvas.robot.numJoint - 1 )
        self.tempPopup.temmpPopup.JointhValue.valueChanged.connect( self.adaptJointID )
    
        self.coverPopup(listAction[self.editName])
        self.currentAction = 'Edit'
        self.tempPopup.temmpPopup.ActionNameLabel.setReadOnly(True)
        self.tempPopup.temmpPopup.ActionButton.clicked.connect(self.saveAction)
        self.tempPopup.temmpPopup.exec()

    def checkAction(self, _name, _jointId, _jointValue, _jointType, _moveType):
        if (self.currentAction == 'Add') and (_name in listActionNameOrigin): raise Exception("Duplicate Name")
        if not(self.canvas.robot.check_limitId(_jointId, _jointValue)): raise Exception("Joint Value wrong")
        if (_jointType) and (self.canvas.robot.jointType[_jointId] == 'l'): raise Exception("Joint Type wrong")
        if not(_jointType) and (self.canvas.robot.jointType[_jointId] == 'r'): raise Exception("Joint Type wrong")
        return True

    def saveAction(self, clickedButton):
        if clickedButton == \
                    self.tempPopup.temmpPopup.ActionButton.button(QtWidgets.QDialogButtonBox.Reset):
            print("Reset Now")
            if (self.currentAction == 'Edit'):
                self.coverPopup(listAction[self.editName])
        elif clickedButton == \
                    self.tempPopup.temmpPopup.ActionButton.button(QtWidgets.QDialogButtonBox.Cancel):
            print("Cancel Successful")
            self.tempPopup.temmpPopup.reject()
            if (self.currentAction == 'Edit'): self.editId = -1
        elif clickedButton == \
                    self.tempPopup.temmpPopup.ActionButton.button(QtWidgets.QDialogButtonBox.Save):

            # Check for correctness
            try:
                currentName = self.tempPopup.temmpPopup.ActionNameLabel.text()
                self.checkAction( currentName, self.tempPopup.temmpPopup.JointhValue.value(), self.tempPopup.temmpPopup.JointhTargetValue.value(),\
                            self.tempPopup.temmpPopup.RevoluteRadioButton.isChecked(), self.tempPopup.temmpPopup.UnionRadioButton.isChecked())
                listAction[currentName] = robot_class.JointAction(currentName, self.tempPopup.temmpPopup.JointhValue.value(),\
                                                            'union' if self.tempPopup.temmpPopup.UnionRadioButton.isChecked() else 'lock' , self.tempPopup.temmpPopup.JointhTargetValue.value(), self.tempPopup.temmpPopup.SpeedValue.value() )
                
                if (self.currentAction == 'Add'):

                    newItem = QtWidgets.QListWidgetItem(currentName, type = 404)
                    if (self.tempPopup.temmpPopup.UnionRadioButton.isChecked()):
                        newItem.setIcon(QtGui.QIcon("chain.png"))
                    else:
                        newItem.setIcon(QtGui.QIcon("lock.png"))

                    listActionName.append(currentName)
                    listActionNameOrigin.append(currentName)
                    with open('Action.txt', 'a') as file:
                        file.write(f'{currentName} {self.tempPopup.temmpPopup.JointhValue.value()} {"union" if self.tempPopup.temmpPopup.UnionRadioButton.isChecked() else "lock"} {self.tempPopup.temmpPopup.JointhTargetValue.value()} {self.tempPopup.temmpPopup.SpeedValue.value()}\n')
                    self.tempPopup.listWidgetActionBasic.addItem(newItem)
                    # self.tempPopup.listWidgetActionBasic.clear()
                    # self.display_file_content()
                    
                elif (self.currentAction == 'Edit'):
                    assert(self.editName == currentName)
                    item = self.ListActionView.findItems(currentName,Qt.Qt.MatchExactly)[0]

                    if (self.tempPopup.temmpPopup.UnionRadioButton.isChecked()):
                        item.setIcon(QtGui.QIcon("chain.png"))
                    else:
                        item.setIcon(QtGui.QIcon("lock.png"))

                # self.tempPopup.temmpPopup.reject()
            except Exception as eMessage:
                print(eMessage)
                self.tempPopup.temmpPopup.ErrorLabel.setText(str(eMessage))

    def openAddZip(self):
        self.tempPopup.temmpPopup = AddZip()
        for i in entries:
            self.tempPopup.temmpPopup.cbo.addItem(i)

        self.tempPopup.temmpPopup.btnAdd.clicked.connect(self.skipActionPart)
        self.tempPopup.temmpPopup.btnBox.clicked.connect(self.addActionPart)
        self.tempPopup.temmpPopup.exec()

    def skipActionPart(self):
        currentName = self.tempPopup.temmpPopup.cbo.currentText()
        self.tempPopup.temmpPopup.lwdActionPart.addItem(currentName)
        # robot_class.Zip.addAction(listAction[currentName])

    def addActionPart(self, clickedButton):
        if clickedButton == \
                    self.tempPopup.temmpPopup.btnBox.button(QtWidgets.QDialogButtonBox.Cancel):
            print("Cancel Zip Successful")
            self.tempPopup.temmpPopup.reject()
        elif clickedButton == \
                    self.tempPopup.temmpPopup.btnBox.button(QtWidgets.QDialogButtonBox.Ok):
            try:
                currentZipName = self.tempPopup.temmpPopup.txtNameAction.toPlainText()
                listZipName.add(currentZipName)
                listZip[currentZipName] = robot_class.Zip(currentZipName)
                
                lwdActionPart = self.tempPopup.temmpPopup.lwdActionPart
                for index in range(lwdActionPart.count()):
                    action = listAction[lwdActionPart.item(index).text()]
                    listZip[currentZipName].addAction(action)
                print('Zip:', listZip)
                self.ListActionView.addItem(currentZipName)
                self.tempPopup.temmpPopup.reject()
            except Exception as eMessage:
                print(eMessage)

    def pre_execute(self):
        if (self.ExecuteActionButton.text() == "Execute"):

            self.endpoint.clearContents()
            self.endpoint.setRowCount(0)

            self.execute()
            self.canvas.robot_limit_plot()
            self.ExecuteActionButton.setText("Pause")
        elif (self.ExecuteActionButton.text() == "Pause"):
            self.canvas.plot_pause()
            self.ExecuteActionButton.setText("Execute")

    def execute(self):
        POSE_TYPE = 808
        JOINT_TYPE = 404
        ACTION_TYPE = 202
        LOCK_TYPE = 101

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
            print('Type:',tempDict[index].type())
            if tempDict[index].type() == POSE_TYPE:
                tempGroup.append(self.canvas.List_Pose[tempDict[index].text()])
            elif tempDict[index].type() == JOINT_TYPE:
                tempGroup.append(listAction[tempDict[index].text()])
            elif tempDict[index].type() == LOCK_TYPE:
                tempGroup.append(listLock[tempDict[index].text()])
            else:
                tempGroup.append(listZip[tempDict[index].text()])

        print('tempGroup:', tempGroup)    

        timeTable = robot_class.TimeTable(self.canvas.robot.numJoint, self.canvas.robot.QHome)
        timeTable.prepare(tempGroup)

        # print("CHECK ROBOT")
        # print(self.canvas.robot.Q)
        self.canvas.setJointTrajectory(timeTable.gen_jointList())

if __name__ == "__main__":
    # Tạo các đối tượng cho màn hình chính
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
