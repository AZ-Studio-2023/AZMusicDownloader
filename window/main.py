# coding:utf-8
import json, sys
import os

from Interface.searchmusic import searchmusic
from Interface.settings import SettingInterface

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication

from qfluentwidgets import NavigationItemPosition, MSFluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
from Interface.localmusics import localmusics
from Interface.playlist import playlist
from Interface.plugin import plugins
from helper.config import cfg,pfg
from helper.pluginHelper import run_plugins, load_plugins
from helper.loggerHelper import logger

api = cfg.ncma_api.value
q_api = cfg.qqma_api.value

# Print logs | 日志输出
logger.info("欢迎使用AZMusicDownloader")
if cfg.beta.value:
    logger.warning("Beta实验功能：启用")
else:
    logger.warning("Beta实验功能：禁用")
logger.debug("Debug模式：启用")
logger.debug("使用的NeteaseCloudMusicApi：" + api)
if q_api:
    logger.debug("使用的QQMusicApi：" + q_api)
else:
    if cfg.debug_card.value:
        logger.warning("使用的QQMusicApi：" + "没有配置")
logger.debug("选择的API："+pfg.apicard.value)
logger.debug(f"显示语言：{cfg.language.value}")

class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(searchmusic(), FIF.SEARCH, '搜索下载')
        self.addSubInterface(localmusics(), FIF.MUSIC_FOLDER, '我的音乐库')
        if cfg.beta.value:
            self.addSubInterface(playlist(), FIF.EXPRESSIVE_INPUT_ENTRY, '歌单')
        if cfg.PluginEnable.value:
            self.addSubInterface(plugins(), FIF.TILES, '插件', position=NavigationItemPosition.BOTTOM)
            load_plugins(parent=self)
            run_plugins(parent=self)
        self.addSubInterface(SettingInterface(), FIF.SETTING, '设置', position=NavigationItemPosition.BOTTOM)
    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('AZMusicDownloader')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        
    def closeEvent(self, event):
        sys.exit(0)
