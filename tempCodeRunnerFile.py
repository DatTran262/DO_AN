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
