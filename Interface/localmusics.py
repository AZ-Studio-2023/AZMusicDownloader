# coding: utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import ListWidget
import os
from qfluentwidgets import ToolButton, PrimaryToolButton
from qfluentwidgets import FluentIcon as FIF
import subprocess
from helper.config import cfg
from helper.inital import mkf

path = cfg.get(cfg.downloadFolder)
mkf()
def get_all_music():
    all_music = []
    path = cfg.get(cfg.downloadFolder)
    for file_name in os.listdir(path):
        if file_name.endswith(".mp3"):
            all_music.append(file_name)
    return all_music

class localmusics(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setObjectName("localmusics")
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.listWidget = ListWidget(self)

        # self.listWidget.setAlternatingRowColors(True)
        self.data = get_all_music()
        stands = self.data
        for stand in stands:
            item = QListWidgetItem(stand)
            # item.setIcon(QIcon(':/qfluentwidgets/images/logo.png'))
            # item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)
        
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.listWidget.clicked.connect(self.openbutton)
        self.resize(300, 400)
        self.openmusic = PrimaryToolButton(FIF.EMBED,self)
        self.openmusic.setEnabled(False)
        self.openmusic.released.connect(self.openthemusic)
        # self.open_dir = ToolButton(FIF.MUSIC_FOLDER, self)
        # self.open_dir.setEnabled(True)
        # self.open_dir.clicked.connect(self.openfolder)
        self.refmusics = ToolButton(FIF.SYNC, self)
        self.refmusics.setEnabled(True)
        self.refmusics.clicked.connect(self.ref)
        
        self.vBoxLayout.addStretch(1)  
        self.vBoxLayout.addWidget(self.openmusic)
        self.vBoxLayout.addStretch(1) 
        # self.vBoxLayout.addWidget(self.open_dir)
        # self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.refmusics)
        self.vBoxLayout.addStretch(20) 
        self.hBoxLayout.addWidget(self.listWidget)
        self.hBoxLayout.addStretch(20)  
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addStretch(1)  
        
        
    def openbutton(self):
        self.openmusic.setEnabled(True)
        
    def openthemusic(self):
        row = self.listWidget.currentIndex().row() 
        name = self.data[row]
        file_path = os.path.join(cfg.get(cfg.downloadFolder), name)
        cmd = f'start "" "{file_path}"'
        subprocess.Popen(cmd, shell=True)

    # def openfolder(self):
    #     f_path = cfg.get(cfg.downloadFolder)
    #     cmd = f'start {f_path}'
    #     print(cmd)
    #     subprocess.Popen(cmd, shell=True)

    def ref(self):
        self.listWidget.clear()
        self.data = get_all_music()
        stands = self.data
        for stand in stands:
            item = QListWidgetItem(stand)
            self.listWidget.addItem(item)