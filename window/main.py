# coding:utf-8
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import MSFluentWindow, NavigationItemPosition

from Interface.localmusics import localmusics
from Interface.playlist import playlist
from Interface.plugin import plugins
from Interface.searchmusic import searchmusic
from Interface.settings import SettingInterface
from helper.config import cfg, pfg
from helper.loggerHelper import logger
from helper.pluginHelper import run_plugins, load_plugins
from helper.getvalue import VERSION, UPDATE_ORDER

api = cfg.ncma_api.value
q_api = cfg.qqma_api.value

# Print logs | 日志输出
logger.info("欢迎使用AZMusicDownloader")
logger.info(f"程序版本：{VERSION}")
logger.info(f"更新编号：{UPDATE_ORDER}")
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
logger.debug(f"默认下载音质：{cfg.level.value}")

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
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('AZMusicDownloader')
        screen_resolution = QDesktopWidget().screenGeometry()
        screen_width = screen_resolution.width()
        screen_height = screen_resolution.height()
        window_width = int(screen_width * 0.46875)
        window_height = int(screen_height * 0.64815)
        self.resize(window_width, window_height)
        self.center()

    def center(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        screen_width = screen_resolution.width()
        screen_height = screen_resolution.height()
        x = (screen_width - self.width()) // 2
        y = (screen_height - self.height()) // 2
        self.move(x, y)
    def closeEvent(self, event):
        sys.exit(0)
