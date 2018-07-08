
# networkscanner
# 一、 介绍
设计一个简单的目录、WEB指纹、端口等扫描程序，判断主机的相应端口的开放情况，扫描发现敏感信息，从而达到信息收集的目的。
# 二、 截图
## 2.1 目录扫描
！[](https://github.com/hannoch/Network-Scanner/blob/master/networkscanner/Screenshot/DirectoryScan.png)
## 2.1 web指纹
！[](https://github.com/hannoch/Network-Scanner/blob/master/networkscanner/Screenshot/WebFingerprint.png)
## 2.1 端口扫描
！[](https://github.com/hannoch/Network-Scanner/blob/master/networkscanner/Screenshot/PortScanner.png)
## 2.1 域名解析
！[](https://github.com/hannoch/Network-Scanner/blob/master/networkscanner/Screenshot/Domian.png)

# 三、工具
## 3.1  开发工具
`python3.6.3、pychram、pyqt5、qt designer`
## 3.2  安装依赖
`pip install -r requeriments.txt`
## 3.3 下载文件
`git clone https://github.com/hannoch/Network-Scanner.git`

# 四、存在的问题
## 4.1  添加代码
每次更新mainwindows.ui文件都要在后面添加一些代码
```
    def percent(self, finished, total, per):
        self.finished_lineEdit.setText(str(finished))
        self.all_lineEdit.setText(str(total))
        self.progressBar.setValue(per)
```
![](https://github.com/hannoch/Network-Scanner/blob/master/networkscanner/Screenshot/addcode.png)
## 4.2 mokey.patch_all()出处问题
这个问题参考了各种资料都没有解决
` MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors, including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3.7. Please monkey-patch earlier. See https://github.com/gevent/gevent/issues/1016. Modules that had direct imports (
`

# 五、参考资料
## 5.1 Web Content Discovery Tool
https://github.com/deibit/cansina  
## 5.2 WebEye
https://github.com/zerokeeper/WebEye
## 5.3 PortScanner
https://github.com/YaokaiYang-assaultmaster/PythonPortScanner
## 5.4 Python安全小工具之Web目录扫描器
https://blog.csdn.net/ski_12/article/details/78443601
## 5.5 DNS处理模块dnspython
https://www.cnblogs.com/stonerainjc/p/6357706.html
## 5.6 Pycharm+Python+PyQt5使用
https://www.cnblogs.com/dalanjing/p/6978373.html


