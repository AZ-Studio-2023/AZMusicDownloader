# coding:utf-8
from helper.config import cfg
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, CustomColorSettingCard,
                            OptionsSettingCard, PushSettingCard, setTheme, isDarkTheme,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea, PushButton,
                            ComboBoxSettingCard, ExpandLayout, Theme, InfoBar, FlyoutView, Flyout)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog
from sys import platform, getwindowsversion
from helper.getvalue import YEAR, AUTHOR, VERSION, HELP_URL, FEEDBACK_URL, RELEASE_URL, autopath, AZ_URL
from helper.inital import delfin

class SettingInterface(ScrollArea):
    musicFoldersChanged = pyqtSignal(list)
    acrylicEnableChanged = pyqtSignal(bool)
    downloadFolderChanged = pyqtSignal(str)
    minimizeToTrayChanged = pyqtSignal(bool)
    micaEnableChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.setObjectName('settings')
        self.settingLabel = QLabel(self.tr("设置"), self)
        
        # Personalize
        self.personalGroup = SettingCardGroup(self.tr('个性化'), self.scrollWidget)
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
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language for UI'),
            texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
            parent=self.personalGroup
        )
        self.micaCard = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr('Mica effect'),
            self.tr('Apply semi transparent to windows and surfaces'),
            cfg.micaEnabled,
            self.personalGroup
        )

        # Folders
        self.DownloadSettings = SettingCardGroup(self.tr("下载设置"), self.scrollWidget)
        self.downloadFolderCard = PushSettingCard(
            self.tr('选择目录'),
            FIF.DOWNLOAD,
            self.tr("下载目录"),
            cfg.get(cfg.downloadFolder),
            self.DownloadSettings
        )
        self.FolderAuto = PushSettingCard(
            self.tr('恢复默认'),
            FIF.DOWNLOAD,
            self.tr("恢复下载目录默认值"),
            self.tr('下载目录默认值为：') + autopath + self.tr('（即用户音乐文件夹）'),
            self.DownloadSettings
        )

        # Application
        self.appGroup = SettingCardGroup(self.tr('应用程序设置'), self.scrollWidget)
        self.beta = SwitchSettingCard(
            FIF.DEVELOPER_TOOLS,
            self.tr('Beta实验功能'),
            self.tr('开启后会启用实验功能'),
            configItem=cfg.beta,
            parent=self.appGroup
        )
        self.Update_Card = SwitchSettingCard(
            FIF.FLAG,
            self.tr('禁用更新检查'),
            self.tr('开启后启动将不会检查版本更新'),
            configItem=cfg.update_card,
            parent=self.appGroup
        )
        self.backtoinit = PushSettingCard(
            self.tr('重置'),
            FIF.CANCEL,
            self.tr("重置应用"),
            self.tr('重置操作重启后生效'),
            self.appGroup
        )

        # Search
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

        # About
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
            self.tr('Changelog'),
            FIF.INFO,
            self.tr('更新日志'),
            '© ' + self.tr(' ') + f" {YEAR}, {AUTHOR}. " +
            self.tr('Version') + f" {VERSION}",
            self.aboutGroup
        )
        
        self.languageCard.setEnabled(False)
        self.micaCard.setEnabled(platform == 'win32' and getwindowsversion().build >= 22000)
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
        self.DownloadSettings.addSettingCard(self.downloadFolderCard)
        self.DownloadSettings.addSettingCard(self.FolderAuto)

        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.languageCard)
        self.personalGroup.addSettingCard(self.micaCard)

        self.appGroup.addSettingCard(self.beta)
        self.appGroup.addSettingCard(self.Update_Card)
        self.appGroup.addSettingCard(self.backtoinit)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)
        
        self.searchGroup.addSettingCard(self.twitCard)
        self.searchGroup.addSettingCard(self.hotCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.DownloadSettings)
        self.expandLayout.addWidget(self.searchGroup)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.appGroup)
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
            self.tr('设置需要重启程序后生效'),
            parent=self.window()
        )

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return
        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)
        
    def __FolederAutoCardClicked(self):
        cfg.set(cfg.downloadFolder, autopath)
        self.downloadFolderCard.setContent(cfg.get(cfg.downloadFolder))
        
    def __backtoinitClicked(self):
        delfin()
        self.__showRestartTooltip()

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)

        # chang the theme of setting interface
        self.__setQss()
        
    def opengithub(self):
        QDesktopServices.openUrl(QUrl(RELEASE_URL))
    def openaz(self):
        QDesktopServices.openUrl(QUrl(AZ_URL))
        
    def __changelog(self):
        view = FlyoutView(
            title='AZMusicDownloader V2.4.2更新日志 ',
            content="1.添加版本检查功能，重大更新不再错过\n2.删除了仅存的搜索页广告，当前全局无广告！\n3.为AZMusicDownloader制作LOGO，全局替换新LOGO",
            #image='resource/splash.png',
            isClosable=True
        )
        
        # add button to view
        button1 = PushButton(FIF.GITHUB, 'GitHub')
        button1.setFixedWidth(120)
        button1.clicked.connect(self.opengithub)
        view.addWidget(button1, align=Qt.AlignRight)
        
        button2 = PushButton('AZ Studio')
        button2.setFixedWidth(120)
        button2.clicked.connect(self.openaz)
        view.addWidget(button2, align=Qt.AlignRight)

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.addSpacing(5)

        # show view
        w = Flyout.make(view, self.aboutCard, self)
        view.closed.connect(w.close)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        cfg.themeChanged.connect(self.__onThemeChanged)
        self.micaCard.checkedChanged.connect(self.micaEnableChanged)

        self.downloadFolderCard.clicked.connect(self.__onDownloadFolderCardClicked)
        self.FolderAuto.clicked.connect(self.__FolederAutoCardClicked)
        self.backtoinit.clicked.connect(self.__backtoinitClicked)
        self.beta.checkedChanged.connect(self.minimizeToTrayChanged)
        self.aboutCard.clicked.connect(self.__changelog)
        self.feedbackCard.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
