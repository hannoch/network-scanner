class WorkThread(QThread):
    # 定义一个信号
    trigger = pyqtSignal()

    def __int__(self):
        # 初始化函数，默认
        super(WorkThread, self).__init__()

    def run(self):
        time.sleep(2)
        # 等待1秒后，给触发信号
        self.trigger.emit()


item = self.result_tableWidget.setColumnWidth(0, 700)
item = self.result_tableWidget.setColumnWidth(1, 60)

self.tableView_set()


def tableView_set(self):
    self.model = QtGui.QStandardItemModel(self.reuslt_tableView)
    self.model.setRowCount(60)
    self.model.setColumnCount(2)
    self.model.setHeaderData(0, QtCore.Qt.Horizontal, "可能存在的地址")
    self.model.setHeaderData(1, QtCore.Qt.Horizontal, "STATUS")
    self.reuslt_tableView.setModel(self.model)
    self.reuslt_tableView.setColumnWidth(0, 620)
    # self.tableView.setColumnWidth(1,250)
    self.reuslt_tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)


def insert_data(self, row, url, status):
    row_count = self.result_tableWidget.rowCount()
    self.result_tableWidget.insertRow(row_count)
    newItem_url = QtWidgets.QTableWidgetItem(url)
    newItem_status = QtWidgets.QTableWidgetItem(str(status))
    self.result_tableWidget.setItem(row, 0, newItem_url)
    self.result_tableWidget.setItem(row, 1, newItem_status)


def percent(self, finished, total, per):
    self.finished_lineEdit.setText(str(finished))
    self.all_lineEdit.setText(str(total))
    self.progressBar.setValue(per)

