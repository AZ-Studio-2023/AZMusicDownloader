# coding: utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QListWidget, QWidget, QHBoxLayout, QLabel

from qfluentwidgets import ListView, setTheme, Theme, ListWidget
import os
from qfluentwidgets import TableWidget, isDarkTheme, setTheme, Theme, TableView, TableItemDelegate, SearchLineEdit, PrimaryPushButton, SpinBox, InfoBar, InfoBarPosition, InfoBarManager, InfoBarIcon,PushButton


def getallmusic():
    allmusic=[]
    musicpath = os.path.join(os.path.expanduser('~'), 'Music')
    path="{}\\AZMusicDownload".format(musicpath)
    for file_name in os.listdir(path):
        allmusic.append(file_name)
    return allmusic

class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setObjectName("Demo")
        self.hBoxLayout = QHBoxLayout(self)
        self.listWidget = ListWidget(self)

        # self.listWidget.setAlternatingRowColors(True)
        self.data = getallmusic()
        stands = self.data
        for stand in stands:
            item = QListWidgetItem(stand)
            # item.setIcon(QIcon(':/qfluentwidgets/images/logo.png'))
            # item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)
        self.empty1 = QLabel('', self)
        self.empty2 = QLabel('', self)
        self.empty3 = QLabel('', self)
        self.empty4 = QLabel('', self)
        self.empty5 = QLabel('', self)
        self.empty6 = QLabel('', self)
        self.empty7 = QLabel('', self)
        self.empty8 = QLabel('', self)
        self.empty9 = QLabel('', self)
        self.empty10 = QLabel('', self)
        self.empty11 = QLabel('', self)
        self.empty12 = QLabel('', self)
        self.empty13 = QLabel('', self)
        self.empty14 = QLabel('', self)
        self.empty15 = QLabel('', self)
        self.empty16 = QLabel('', self)
        self.empty17 = QLabel('', self)
        self.empty18 = QLabel('', self)
        self.empty19 = QLabel('', self)
        self.empty20 = QLabel('', self)
        self.empty21 = QLabel('', self)
        self.empty22 = QLabel('', self)
        self.empty23 = QLabel('', self)
        self.empty24 = QLabel('', self)
        self.hBoxLayout.addWidget(self.empty19)
        self.hBoxLayout.addWidget(self.empty20)
        self.hBoxLayout.addWidget(self.empty21)
        self.hBoxLayout.addWidget(self.empty22)
        self.hBoxLayout.addWidget(self.empty23)
        self.hBoxLayout.addWidget(self.empty24)
        self.hBoxLayout.addWidget(self.empty13)
        self.hBoxLayout.addWidget(self.empty14)
        self.hBoxLayout.addWidget(self.empty15)
        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.listWidget)
        self.listWidget.clicked.connect(self.openbutton)
        self.resize(300, 400)
        self.openmusic = PrimaryPushButton("打开",self)
        self.openmusic.setEnabled(False)
        self.openmusic.released.connect(self.openthemusic)
        self.hBoxLayout.addChildWidget(self.openmusic)
    def openbutton(self):
        self.openmusic.setEnabled(True)
    def openthemusic(self):
        row = self.listWidget.currentIndex().row() 
        name = self.data[row]
        musicpath = os.path.join(os.path.expanduser('~'), 'Music')
        print("{}\\AZMusicDownload\\{}".format(musicpath,name))
if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
