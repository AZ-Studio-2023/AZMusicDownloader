# coding:utf-8
import json
import random

import requests

from helper.config import cfg, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard, InfoBarPosition,
                            OptionsSettingCard, RangeSettingCard, PushSettingCard, InfoBarIcon, PushButton,
                            ColorSettingCard, HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, InfoBar, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths, QThread, pyqtSlot
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFontDialog, QFileDialog
from json import loads
import webbrowser
import datetime

YEAR = int(datetime.date.today().year)
AUTHOR = "AZ Studio"
VERSION = "2.0.0 Fix"
HELP_URL = "https://azstudio.net.cn/"
FEEDBACK_URL = "https://azstudio.net.cn/"
RELEASE_URL = "https://azstudio.net.cn/"

def getad():
    url = "https://json.zenglingkun.cn/ad/music/setting.json"
    try:
        ad = requests.get(url).text
        data = loads(ad)
        msg = data
    except:
        try:
            o = open("resource/hitokoto.json", "r")
            hit_data = json.loads(o.read())["hitokoto"]
            o.close()
            poem = hit_data[random.randint(0, len(hit_data) - 1)]
        except:
            poem = "海内存知己，天涯若比邻"
        ad = {"title": "(⊙o⊙)？", "text": "呀！找不到广告了 ＞﹏＜ 请检查您的网络连接\n{}".format(poem), "time": 30000,
              "button": "（；´д｀）ゞ", "url": "https://azstudio.net.cn"}
        msg = ad
    return msg

class get_ad(QThread):
    finished = pyqtSignal(dict)

    @pyqtSlot()
    def run(self):
        data = getad()
        self.finished.emit(data)

class SettingInterface(ScrollArea):
    """ Setting interface """
    def openlk(self):
        webbrowser.open_new_tab(self.ad_list("url"))
    checkUpdateSig = pyqtSignal()
    musicFoldersChanged = pyqtSignal(list)
    acrylicEnableChanged = pyqtSignal(bool)
    downloadFolderChanged = pyqtSignal(str)
    minimizeToTrayChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.setObjectName('settings')
        # setting label

        self.settingLabel = QLabel(self.tr("设置"), self)
        #self.illustrate = SettingCardGroup(self.tr('所有设置项都需重启程序才能生效噢'), self.scrollWidget)
        # music folders

        self.personalGroup = SettingCardGroup(self.tr('主题'), self.scrollWidget)
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('深浅模式'),
            self.tr("更改应用程序的外观"),
            texts=[
                self.tr('浅色'), self.tr('深色'),
                self.tr('使用系统设置')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard=CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('主题颜色'),
            self.tr('更改应用程序的主题颜色'),
            self.personalGroup
        )

        

        self.appGroup = SettingCardGroup(self.tr('应用程序设置'), self.scrollWidget)
        self.beta = SwitchSettingCard(
            FIF.DEVELOPER_TOOLS,
            self.tr('Beta实验功能'),
            self.tr('开启后会启用实验功能'),
            configItem=cfg.beta,
            parent=self.appGroup
        )
        self.adCard = SwitchSettingCard(
            FIF.CALORIES,
            self.tr('关闭广告'),
            self.tr('这是我们目前唯一的收入来源，求求别关闭qwq，如果真的要关闭的话，得重启后才能生效'),
            configItem=cfg.adcard,
            parent=self.appGroup
        )

        self.searchGroup = SettingCardGroup(self.tr('搜索设置'), self.scrollWidget)
        self.twitCard = SwitchSettingCard(
            FIF.TAG,
            self.tr('搜索时展示相关的预选项'),
            self.tr('关闭后会更加节省资源'),
            configItem=cfg.twitcard,
            parent=self.searchGroup
        )
        self.twitCard.setEnabled(False)
        self.hotCard = SwitchSettingCard(
            FIF.TAG,
            self.tr('搜索时展示热门歌曲预选项'),
            self.tr('关闭后启动会更快'),
            configItem=cfg.hotcard,
            parent=self.searchGroup
        )

        # application
        self.aboutGroup = SettingCardGroup(self.tr('关于'), self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            self.tr('打开帮助页面'),
            FIF.HELP,
            self.tr('帮助'),
            self.tr('从帮助页面上获取帮助与支持'),
            self.aboutGroup
        )
        self.feedbackCard = PrimaryPushSettingCard(
            self.tr('提供反馈'),
            FIF.FEEDBACK,
            self.tr('提供反馈'),
            self.tr('通过提供反馈来帮助我们打造更好的应用'),
            self.aboutGroup
        )
        self.aboutCard = PrimaryPushSettingCard(
            self.tr('AZ Studio'),
            FIF.INFO,
            self.tr('关于'),
            '© ' + self.tr(' ') + f" {YEAR}, {AUTHOR}. " +
            self.tr('Version') + f" {VERSION}",
            self.aboutGroup
        )
        self.adw = get_ad()
        if cfg.adcard.value == False:
            self.adw.start()
        self.adw.finished.connect(self.show_ad)
        self.__initWidget()


    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize style sheet
        self.__setQss()

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(60, 63)
        
        # add cards to group
        

        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)

        self.appGroup.addSettingCard(self.beta)
        self.appGroup.addSettingCard(self.adCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)
        
        self.searchGroup.addSettingCard(self.twitCard)
        self.searchGroup.addSettingCard(self.hotCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.appGroup)
        self.expandLayout.addWidget(self.searchGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{theme}/setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.warning(
            '',
            self.tr('Configuration takes effect after restart'),
            parent=self.window()
        )

    def __onDeskLyricFontCardClicked(self):
        """ desktop lyric font button clicked slot """
        font, isOk = QFontDialog.getFont(
            cfg.desktopLyricFont, self.window(), self.tr("Choose font"))
        if isOk:
            cfg.desktopLyricFont = font

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)

        # chang the theme of setting interface
        self.__setQss()

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        cfg.themeChanged.connect(self.__onThemeChanged)

        # music in the pc
        

        # personalization

        # playing interface
        

        # main panel
        self.beta.checkedChanged.connect(
            self.minimizeToTrayChanged)

        # about
        self.aboutCard.clicked.connect(self.checkUpdateSig)
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
    def show_ad(self, ad_v):
        self.ad_list = ad_v
        self.ad = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title=self.ad_list["title"],
            content=self.ad_list["text"],
            orient=Qt.Vertical,  # vertical layout
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=self.ad_list["time"],
            parent=self
        )
        self.s = PushButton(self.ad_list["button"])
        self.s.clicked.connect(self.openlk)
        self.ad.addWidget(self.s)
        self.ad.show()
        self.adw.quit()
