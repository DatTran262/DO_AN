    def addActionPart(self, clickedButton):
        if clickedButton == self.tempPopup.btnBox.button(QtWidgets.QDialogButtonBox.Cancel):
            print("Cancel Zip Successful")
            self.tempPopup.reject()
        elif clickedButton == self.tempPopup.btnBox.button(QtWidgets.QDialogButtonBox.Ok):
            try:
                currentZipName = self.tempPopup.txtNameAction.toPlainText()
                if currentZipName in listZipName:
                    raise ValueError('Ten da ton tai.')
                listZipName.add(currentZipName)
                listZip[currentZipName] = robot_class.Zip(currentZipName)
                for index in range(self.tempPopup.lwdActionPart.count()):
                    action = listAction[self.tempPopup.lwdActionPart.item(index).text()]
                    listZip[currentZipName].addAction(action)
                self.ListActionView.addItem(currentZipName)
                self.tempPopup.reject()  # Chỉ đóng cửa sổ nếu không có lỗi
            except Exception as eMessage:
                error_message = str(eMessage)
                if currentZipName in listZipName:
                    error_message = 'Tên đã tồn tại. Vui lòng chọn tên khác.'
                QMessageBox.critical(self, 'Lỗi', error_message)