import _thread
import os
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import subprocess
import resource_rc
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextBrowser, QLabel, QDialog, QTextEdit, \
    QMessageBox

from MainFunction.main import Opt, f
from TrainModel.MRF_Main import TrainInterface


class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))
class BaseWindow(QDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.hide()
    def outputWritten(self, text):
        if('/' in text):
            return
        # cursor = self.textBrowser.textCursor()
        # cursor.movePosition(QtGui.QTextCursor.End)
        # self.textBrowser.show()
        #
        # cursor.insertText(text)
        self.textBrowser.insertPlainText(text)
        QtWidgets.QApplication.processEvents()
    def setStdout(self):
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        self.textBrowser.show()
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "工具复现！"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 472
        self.TextStyle = """
        padding-left: 10px;
        padding-right: 10px;
        padding-top: 1px;
        padding-bottom: 1px;
        color: #fff;
        background: transparent;
        """
        self.FunctionStyle = """
                padding-left: 10px;
                padding-right: 10px;
                padding-top: 1px;
                padding-bottom: 1px;
                color: #fff;
                background: transparent;
                font:15px
                """
        self.ButtonSyle = """
                text-align : center;

                font : 14px;
                background: transparent;

        """
        self.image = QImage(":/BackGround.jpg")
        # self.setMovie(self.image)
        self.use_palette()



        self.Introduction = QTextBrowser(self)
        self.Introduction.setText(
            "本工具功能是减轻西班牙语中性别刻板印象的数据扩增\n代码链接：https://github.com/xiaoyaoing/Automated-test-tool-replication\n ")
        self.Introduction.setGeometry(0, 10, 800, 40)
        self.Introduction.setStyleSheet(self.TextStyle)


        self.function1 = QTextBrowser(self)
        self.Button1 = QPushButton(self)
        self.Button1.setText("点击这里执行功能1！！！")
        self.Button1.clicked.connect(self.test)
        self.Button1.setGeometry(200, 70, 200, 30)

        self.function1.setGeometry(0, 70, 800, 30)
        #  t1.setStyleSheet(self.ButtonSyle)
        self.function1.setText("功能1: 转换已有西班牙句子")
        self.function1.setStyleSheet(self.FunctionStyle)


        self.function2 = QTextBrowser(self)
        self.Button2 = QPushButton(self)
        self.Button2.setText("点击这里执行功能2！！！")
        self.Button2.clicked.connect(self.test2)
        self.Button2.setGeometry(200, 100, 200, 30)

        self.function2.setGeometry(0, 100, 800, 30)
        #  t1.setStyleSheet(self.ButtonSyle)
        self.function2.setText("功能2: 训练模型")
        self.function2.setStyleSheet(self.FunctionStyle)
        self.InitWindow()


    def test(self):
        self.function1Dialog=Fucntion1Window(self)
        self.function1Dialog.exec()
    def test2(self):
        self.function2Dialog=Function2Window(self)
        self.function2Dialog.exec()
    def use_palette(self):
        pixmap = QPixmap(":/background2.jpg")
        pixmap.scaled(self.size())
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(pixmap))
        self.setPalette(window_pale)
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()
class Fucntion1Window(BaseWindow):

    def __init__(self,parent):
        super().__init__(parent)
        #self.setParent(parent)
        self.setStdout()
        self.ArgList1=['' for i in range(0,5)]

        self.buttonStyle="""
        background-color: #66CCFF;
        """
        text1="选择输入的conllu文件"
        text2="选择结果输出的conllu文件"
        text3="选择模型文件（如不选择将使用默认模型)"
        text5="选择要改变的名词列表(.tsv)"
        self.texts=[text1,text2,text3,text5]

        self.thr=QThread()

        self.buttonHeight=30
        button1=QPushButton(self)
        button1.clicked.connect(lambda:self.openfile('*.conllu',1))
        button1.setGeometry(0,0,400,self.buttonHeight)
        button1.setStyleSheet(self.buttonStyle)

        button2=QPushButton(self)
        button2.clicked.connect(lambda: self.openfile('*.conllu',2))
        button2.setGeometry(0,self.buttonHeight, 400, self.buttonHeight)
        button2.setStyleSheet(self.buttonStyle)

        button3=QPushButton(self)
        button3.clicked.connect(lambda: self.openfile('*.pt',3))
        button3.setGeometry(0,self.buttonHeight*2,400,self.buttonHeight)
        button3.setStyleSheet(self.buttonStyle)



        button5 = QPushButton(self)
        button5.clicked.connect(lambda: self.openfile('*.tsv',4))
        button5.setGeometry(0, self.buttonHeight*3, 400, self.buttonHeight)
        button5.setStyleSheet(self.buttonStyle)

        self.buttons=[button1,button2,button3,button5]
        self.initButtonText()
        button6=QPushButton(self)
        button6.setText("开始转换")
        button6.clicked.connect(self.f1)
        button6.setGeometry(0, self.buttonHeight * 5, 200, self.buttonHeight)

        button7=QPushButton(self)
        button7.setText("取消转换")
        button7.clicked.connect(self.cancel)
        button7.setGeometry(200,self.buttonHeight*5,200,self.buttonHeight)

        self.textBrowser.setGeometry(0,self.buttonHeight*6,400,400)
        self.textBrowser.setWindowTitle('输出信息')
    def initButtonText(self):
        for i in range(len(self.buttons)):
            self.buttons[i].setText(self.texts[i])
    def openfile(self,type,argType):
        directory = QtWidgets.QFileDialog.getOpenFileName(self,"getOpenFileName", "./",
                                              "Conllu Files ({})".format(type))
        argType = int(argType)
        if(directory[0]!=''):
            self.buttons[argType-1].setText(directory[0])
        self.ArgList1[(argType)-1]=directory
    def cancel(self):
        i=self.thr.isRunning()
        self.thr.quit()
        i=self.thr.isRunning()
    def f1(self):
        # opt=Opt("/Users/yjp/nju/大三上/自动化测试/biasCDA/conllus/test_input.conllu",
        #         "/Users/yjp/nju/大三上/自动化测试/biasCDA/conllus/test_output.conllu",
        #         'none',
        #         "/Users/yjp/nju/大三上/自动化测试/biasCDA/animacy/spanish.tsv"           )
        inFile=self.ArgList1[0]
        outFile=self.ArgList1[1]
        Model=self.ArgList1[2]
        AnimateList=self.ArgList1[3]
        flag1=False
        if(inFile==''):
            QMessageBox.information(self,"提示","待转换的conllu文件还没选择",QMessageBox.Yes)
            return
        if(outFile==''):
            QMessageBox.information(self,"提示","存储结果的conllu文件还没选择",QMessageBox.Yes)
            return
        if(Model==''):
            reply=QMessageBox.question(self,'提示',"你还没有选择模型，是否使用默认模型", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if(reply==QMessageBox.Yes):
                flag1=True
            else:
                return
        if(AnimateList==''):
            QMessageBox.information(self, "提示","名词范围还未选择", QMessageBox.Yes)
            return
        if(flag1):
            Model='none'
        opt = Opt(inFile[0], outFile[0], Model, AnimateList[0])
        self.thr = mythread(opt)
        self.thr.start()

class mythread(QThread):
    def __init__(self,opt):
        super(mythread,self).__init__()
        self.opt=opt
    def run(self):
        f(self.opt)
        return

class Function2Window(BaseWindow):
    def __init__(self,parent):
        super().__init__(parent)
        #self.setParent(parent)
        self.setStdout()
        self.ArgList1=['' for i in range(0,5)]

        self.buttonStyle="""
        background-color: #66CCFF;
        """
        text1="选择数据集文件夹（文件夹下需有-train,-test_input,-dev三种conllu文件"
        text2="选择存储结果的文件夹"

        self.texts=[text1,text2]

        self.thr=QThread()

        self.buttonHeight=30
        button1=QPushButton(self)
        button1.clicked.connect(lambda:self.openfile('*',1))
        button1.setGeometry(0,0,400,self.buttonHeight)
        button1.setStyleSheet(self.buttonStyle)
        button1.setText(text1)
        button2=QPushButton(self)
        button2.clicked.connect(lambda: self.openfile('*',2))
        button2.setGeometry(0,self.buttonHeight, 400, self.buttonHeight)
        button2.setStyleSheet(self.buttonStyle)
        button2.setText(text2)
        self.buttons=[button1,button2]

        button6=QPushButton(self)
        button6.setText("开始训练")
        button6.clicked.connect(self.f1)
        button6.setGeometry(0, self.buttonHeight * 2, 200, self.buttonHeight)

        button7=QPushButton(self)
        button7.setText("取消训练")
        button7.clicked.connect(self.cancel)
        button7.setGeometry(200,self.buttonHeight*2,200,self.buttonHeight)

        self.textBrowser.setGeometry(0,self.buttonHeight*3,400,400)
        self.textBrowser.setWindowTitle('输出信息')

    def openfile(self,type,argType):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,"getOpenFileName", "./")
        argType = int(argType)
        if(directory!=''):
            self.buttons[argType-1].setText(directory)
        self.ArgList1[(argType)-1]=directory

    def f1(self):
        if (self.ArgList1[0] == ''):
            QMessageBox.information(self, "提示", "数据文件夹还没选择", QMessageBox.Yes)
            return
        if (self.ArgList1[0] == ''):
            QMessageBox.information(self, "提示", "输出文件夹还没选择", QMessageBox.Yes)
            return
        self.thr=QThread(self)
        self.thr.start(TrainInterface(self.ArgList1[0],self.ArgList1[1]))
    def cancel(self):
        self.thr.exit(0)