#!/usr/bin/python
#coding=utf-8
import requests
import sys,os
import time
from queue import Queue
import threading
from mainwindow import  Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from DirectoryScan import UserAgentList as UAL
from optparse import OptionParser
from PyQt5 import QtWidgets




class DirScan_Main:
    """docstring for DirScanMain"""
    def __init__(self,UI,options):
        self.url = options['url']
        self.filename = options['filename']
        self.count = options['count']
        self.ui = UI


    class DirScan(threading.Thread):
        """docstring for DirScan"""
        def __init__(self, UI,queue,total):
            threading.Thread.__init__(self)
            self._queue = queue
            self._total = total
            self.ui = UI



        def run(self):
            while not self._queue.empty():
                url = self._queue.get()
                threading.Thread(target=self.msg).start()
                r = requests.get(url=url, headers= UAL.get_user_agent(), timeout=8,)
                if r.status_code == 200:
                    sys.stdout.write('\r' + '[+]%s\t\t\n' % (url))
                    result = open('result.txt','a+')
                    result.writelines(url + '\n')
                    result.close()

 
        def msg(self):
            # print self._total,self._queue.qsize()
            per = 100 - float(self._queue.qsize())/float(self._total) * 100
            finished = self._total - self._queue.qsize()
            percentage = "%s Finished| %s All| Scan in %1.f %s"%(finished,self._total,per,'%')
            self.ui.percent(finished,self._total,per)
            sys.stdout.write('\r'+'[*]'+percentage)


    def start(self):
        result = open('result.html','w')
        result.close()
        queue = Queue()
        file_path = os.path.abspath(os.path.dirname('.'))
        filedirc = open(file_path + '\\DirectoryScan\\Directory\\' + self.filename,'r')
        for i in filedirc:
            queue.put(self.url+i.rstrip('\n'))

        total = queue.qsize()
        threads = []
        thread_count = int(self.count)
 
        for i in range(thread_count):
            threads.append(self.DirScan(self.ui,queue,total))
        for i in threads:
            i.start()
        for i in threads:
            i.join()
