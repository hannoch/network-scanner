import  sys
import dns.resolver
from PyQt5.QtGui import QStandardItemModel

from mainwindow import  Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from DirectoryScan import direscan
from PortScanner import constants
from PortScanner import PortScanner as ps
from WebFingerprint import WebEye as we

class TableData():
    def TableViewInit(self,tableView,Model):
        try:
            self.HeaderList = ["可能存在的地址","STATUS"]
            self.DataModel = Model
            self.DataModel.setHorizontalHeaderLabels(self.HeaderList)  #
            self.tableView = tableView
            self.tableView.setModel(self.DataModel)
            self.tableView.setColumnWidth(0, 620)
            self.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        except Exception as e:
            logging(e)

    def Model_setItem(self, row, column, data):
        '''表格添加数据：第row行，column列数据更改为data'''
        self.DataModel.setItem(row, column, QtGui.QStandardItem(data))
        pass


class mywindow(QMainWindow,Ui_MainWindow):
    TableDataSignal = pyqtSignal(int, int, str)

    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.initUI()
        self.port_list = []
        self.target_ports = 50
        self.TableData = TableData()  # 声明类
        self.Model_Data = QStandardItemModel(60, 2)  # 初始化一个模型QStandardItemModel，4行13列
        self.TableData.TableViewInit(self.reuslt_tableView, self.Model_Data)  # 调用类TableData中初始化表格函数

    def initUI(self):
        self.start_scan_Button.clicked.connect(self.directory_scan)
        self.domain_start_Button.clicked.connect(self.print_domain_info)
        self.port_num_comboBox.currentIndexChanged.connect(self.selection_change)
        self.port_scan_Button.clicked.connect(self.port_work)
        self.web_start_Button.clicked.connect(self.web_fingerpirnt_work)
        #self.TableDataSignal.connect(self.TableData.Model_setItem)  # 这里采用信号槽来绑定Model_setItem进行数据更新
        #self.TableDataSignal.emit(0, 0, 'sdfsdf')  # 这里为表格添加一个数据，信号发送

    def directory_scan(self):
        '''
        构造字典：options = {'url': 'http://192.168.74.133',
                            'filename': 'PHP.txt',
                            'count': 10}
        :return:
        '''
        filename = ''
        if self.php_checkBox.isChecked():
            filename = 'PHP.txt'

        options = {'url': self.url_lineEdit.text(),
                   'filename': filename,
                   'count': self.threads_lineEdit.text()}

        dirscan = direscan.DirScan_Main(self,options)
        dirscan.start()

        result_url =[]
        with open('result.txt','r') as file:
            temp_url = file.readlines()
            result_url = temp_url
        row = 0
        for index in result_url:
            self.TableData.Model_setItem(row,0,index)
            self.TableData.Model_setItem(row, 1, '200')
            row = row + 1
    def emit_print_domain_info(self):
        if self.domain_start_Button.isChecked() == True:
            text1 = self.domain_lineEdit.text()
            print(text1)
            self.print_domain_Signal[str].emit(self.domain_lineEdit.text())
    def print_domain_info(self):
        domain = self.domain_lineEdit.text()
        list_A = []
        A = dns.resolver.query(domain, 'A')  # 指定查询记录为A型
        for index in A.response.answer:  # 通过response.answer方法获取查询回应信息
            for j in index.items:
                list_A.append(str(index))

        a = '\n'.join(list_A)
        self.A_textEdit.setText(a)

        list_MX = []
        MX = dns.resolver.query(domain, 'MX')  # 指定解析类型为MX记录
        for i in MX:  # 遍历回应结果
            strs = 'MX preference =' + str(i.preference) + ' mail exchanger =' + str(i.exchange)
            list_MX.append(strs)
        mx = ','.join(list_MX)
        mx = mx.replace(',','\n')
        self.MX_textEdit.setText(mx)
        #print('NS记录：标记区域的域名服务器及授权子域')
        list_NS = []
        NS = dns.resolver.query(domain, 'NS')
        for i in NS.response.answer:
            for j in i.items:
                list_NS.append(str(i))
        #print(list_NS)
        ns = '\n'.join(list_NS)
        self.NS_textEdit.setText(ns)

    def selection_change(self):

        self.port_scan_Button.setEnabled(bool(True))
        TOP = self.port_num_comboBox.currentText()
        port_list= []
        port_str_top = ''
        if TOP == 'TOP50':
            self.port_list = constants.port_list_top_50
            self.target_ports = 50
            for index in self.port_list:
                port_str_top = port_str_top + str(index) + ','
            self.source_ports_textEdit.setText(port_str_top)
        elif TOP == 'TOP100':
            self.port_list = constants.port_list_top_100
            self.target_ports = 100
            for index in self.port_list:
                port_str_top = port_str_top + str(index) + ','
            self.source_ports_textEdit.setText(port_str_top)
        elif TOP == 'TOP1000':
            self.port_list = constants.port_list_top_1000
            self.target_ports = 1000
            for index in self.port_list:
                port_str_top = port_str_top + str(index) + ','
            self.source_ports_textEdit.setText(port_str_top)
        else:
            pass


    def port_work(self):
        scanner = ps.PortScanner(self.target_ports)
        print(self.target_ports)
        host_name = self.port_ip_lineEdit.text()
        message = 'put whatever message you want here'
        scanner.set_delay(15)
        scanner.show_target_ports()
        scanner.show_delay()
        output = scanner.scan(host_name, message)
        result = ''
        for port in output:
            if output[port] == 'OPEN':
                print('{}: {}\n'.format(port, output[port]))
                temp = str(port) + ':' + str(output[port] + '\n')
                result = result + temp
        #print(result)
        self.result_port_textEdit.setText(result)


    def web_fingerpirnt_work(self):
        web_url = self.web_utl_lineEdit.text()
        print(web_url)
        res = we.web_eye(web_urlurl)
        res.run()
        cms = list(res.cms_list)
        print(cms)

    def msg(self):
        reply = QMessageBox.information(self,'错误','未选择网址程序',QMessageBox.Yes)
        print(reply)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())