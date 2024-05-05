# coding:utf-8

from Interface.searchmusic import searchmusic
from Interface.settings import SettingInterface

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import NavigationItemPosition, MSFluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
from Interface.localmusics import localmusics
from Interface.playlist import playlist
from helper.config import Config

class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(searchmusic(), FIF.CARE_RIGHT_SOLID, '搜索下载')
        self.addSubInterface(localmusics(), FIF.MUSIC_FOLDER, '我的音乐库')
        if Config.beta.value == True:
            self.addSubInterface(playlist(), FIF.EXPRESSIVE_INPUT_ENTRY, '歌单')
        self.addSubInterface(SettingInterface(), FIF.SETTING, '设置', position=NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('AZMusicDownloader')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)





