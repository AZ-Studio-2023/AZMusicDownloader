# coding:utf-8
from helper.LoginHelper import UserLogin
from helper.config import cfg, pfg
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QThreadPool
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog
from sys import platform, getwindowsversion
from helper.getvalue import YEAR, AUTHOR, VERSION, HELP_URL, FEEDBACK_URL, autopath, apilists, \
    audio_quality_list
from helper.inital import delfin, get_update, showup, setSettingsQss
from helper.localmusicsHelper import ref
from helper.SettingHelper import DeleteAllData, editapi
from sys import exit
from helper.flyoutmsg import changelog, restart,setOK

class LoginMessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('登录账号')
        self.type_Label = QLabel("API:", self)
        self.type_Label.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:Microsoft YaHei;}")
        self.type_Box = ComboBox()
        self.type_Box.addItems(["NCMA"])
        self.tipLabel = StrongBodyLabel(self.tr("请在浏览器中扫码登录，大约5-10秒后将打开页面"), self)


        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.type_Label)
        self.viewLayout.addWidget(self.type_Box)
        self.viewLayout.addWidget(self.tipLabel)

        self.login = UserLogin()
        self.pool = QThreadPool()
        self.login.signals.progress.connect(self.refresh)
        self.pool.start(self.login)

        self.widget.setMinimumWidth(350)
    def refresh(self, code):
        if code == 200:
            self.tipLabel.setText("登录成功")
        else:
            self.tipLabel.setText("二维码已过期")

    def stop(self):
        self.pool.clear()

class SettingInterface(ScrollArea):
    micaEnableChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.setObjectName('settings')
        self.settingLabel = QLabel(self.tr("设置"), self)
        self.upworker = get_update()
        self.upworker.finished.connect(lambda updata: showup(parent = self, updata = updata, upworker = self.upworker))
        
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
            self.tr('语言'),
            self.tr('当前仅支持简体中文'),
            texts=['简体中文', self.tr('使用系统设置')],
            parent=self.personalGroup
        )
        self.micaCard = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr('云母效果'),
            self.tr('应用Mica半透明效果（仅支持Windows11）'),
            cfg.micaEnabled,
            self.personalGroup
        )

        # Folders
        self.DownloadSettings = SettingCardGroup(self.tr("下载设置"), self.scrollWidget)
        
        self.downloadFolderCard = ExpandGroupSettingCard(
            FIF.FOLDER,
            self.tr('修改目录'),
            self.tr("修改下载目录"),
            self.personalGroup
        )
        self.LabelFolder = SubtitleLabel(f"\n    当前路径为：{cfg.downloadFolder.value}\n", self)
        self.LabelAuto = SubtitleLabel(f"\n    默认路径为：{autopath}\n", self)
        self.changeFolder = PrimaryPushButton("选择目录", self)
        self.AutoFolder = PushButton("恢复默认", self)
        self.ApiUrlCard = PushSettingCard(
            self.tr('修改'),
            FIF.EDIT,
            self.tr("自定义API地址"),
            self.tr("修改NCMA或QQMA的API地址"),
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
        self.beta.checkedChanged.connect(self.beta_enable)
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
        self.apiCard = ComboBoxSettingCard(
            pfg.apicard,
            FIF.GLOBE,
            self.tr('第三方音乐API'),
            self.tr('仅会修改搜索下载页使用的API。由于QQMA需要账号COOKIE才能进行调用，请自行部署。'),
            texts=apilists,
            parent=self.searchGroup
        )

        self.levelCard = ComboBoxSettingCard(
            pfg.level,
            FIF.ALBUM,
            self.tr('默认下载音质'),
            self.tr('仅对NCMA生效。该项仅保证程序发出的请求无误，无法确保上游API返回的是对应音质的音频。'),
            texts=audio_quality_list,
            parent=self.searchGroup
        )
        self.loginCard = PushSettingCard(
            self.tr('登录'),
            FIF.PEOPLE,
            self.tr('登录音乐平台账号'),
            self.tr('当用户拥有VIP，可在此登录以下载完整音频'),
            parent=self.searchGroup
        )
        self.loginCard.button.clicked.connect(self.showMessage)
        
        #BetaOnly
        if cfg.beta.value:
            self.betaonly()

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
        self.feedbackCard = PushSettingCard(
            self.tr('提供反馈'),
            FIF.FEEDBACK,
            self.tr('提供反馈'),
            self.tr('通过提供反馈来帮助我们打造更好的应用'),
            self.aboutGroup
        )
        self.sponsor = ExpandGroupSettingCard(
            FIF.HEART,
            self.tr("赞助名单"),
            self.tr("给本项目赞助的热心人"),
            self.aboutGroup
        )
        # self.serverCard = HyperlinkCard(
        #     SERVER_URL,
        #     self.tr('领创云'),
        #     FIF.IOT,
        #     self.tr('云计算支持'),
        #     self.tr('本项目由 领创云 提供云计算支持'),
        #     self.sponsor
        # )
        # self.sponsor.addGroupWidget(self.serverCard)
        self.aboutCard = PushSettingCard(
            self.tr('更新日志'),
            FIF.INFO,
            self.tr('关于'),
            '© ' + self.tr(' ') + f" {YEAR}, {AUTHOR}. " +
            self.tr('Version') + f" {VERSION}",
            self.aboutGroup
        )
        
        self.micaCard.setEnabled(False)
        if cfg.beta.value:
            self.toast_Card.setEnabled(platform == 'win32' and getwindowsversion().build >= 17763)
        self.__initWidget()

    def betaonly(self):
        self.BetaOnlyGroup = SettingCardGroup(self.tr('Beta Only'), self.scrollWidget)
        self.debug_Card = SwitchSettingCard(
                FIF.CODE,
                self.tr('Debug Mode'),
                self.tr('The global exception capture will be disabled, and there will be outputs in the commandline.(Code Running Only)'),
                configItem=cfg.debug_card,
                parent=self.BetaOnlyGroup
        )
        self.plugin_Card = SwitchSettingCard(
                FIF.DICTIONARY_ADD,
                self.tr('Enable Plugins'),
                self.tr('You can use more APIs or other features through using plugins.'),
                configItem=cfg.PluginEnable,
                parent=self.BetaOnlyGroup
        )
        self.toast_Card = SwitchSettingCard(
                FIF.MEGAPHONE,
                self.tr('Enable Windows Toast'),
                self.tr(
                    'Use System Notification to notice you when the process is finished. ( Windows 10.0.17763 or later)'),
                configItem=cfg.toast,
                parent=self.BetaOnlyGroup
        )

    def beta_enable(self):
        if cfg.beta.value:
            self.betaonly()
            self.toast_Card.setEnabled(platform == 'win32' and getwindowsversion().build >= 17763)
            self.expandLayout.addWidget(self.BetaOnlyGroup)
            self.BetaOnlyGroup.addSettingCard(self.debug_Card)
            self.BetaOnlyGroup.addSettingCard(self.plugin_Card)
            self.BetaOnlyGroup.addSettingCard(self.toast_Card)
            self.debug_Card.setVisible(True)
            self.plugin_Card.setVisible(True)
            self.toast_Card.setVisible(True)
            self.BetaOnlyGroup.setVisible(True)
        else:
            self.debug_Card.setValue(False)
            self.plugin_Card.setValue(False)
            self.toast_Card.setValue(False)
            self.debug_Card.setVisible(False)
            self.plugin_Card.setVisible(False)
            self.toast_Card.setVisible(False)
            self.BetaOnlyGroup.setVisible(False)
    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        setSettingsQss(parent=self)

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(60, 63)
        
        # ExpandCard
        self.downloadFolderCard.addGroupWidget(self.LabelFolder)
        self.downloadFolderCard.addGroupWidget(self.LabelAuto)
        self.downloadFolderCard.addWidget(self.changeFolder)
        self.downloadFolderCard.addWidget(self.AutoFolder)
        
        # add cards to group
        self.DownloadSettings.addSettingCard(self.downloadFolderCard)
        self.DownloadSettings.addSettingCard(self.ApiUrlCard)

        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.languageCard)
        self.personalGroup.addSettingCard(self.micaCard)

        self.appGroup.addSettingCard(self.beta)
        self.appGroup.addSettingCard(self.Update_Card)
        self.appGroup.addSettingCard(self.backtoinit)
        
        if cfg.beta.value:
            self.BetaOnlyGroup.addSettingCard(self.debug_Card)
            self.BetaOnlyGroup.addSettingCard(self.plugin_Card)
            self.BetaOnlyGroup.addSettingCard(self.toast_Card)

        self.aboutGroup.addSettingCard(self.sponsor)
        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)
        
        self.searchGroup.addSettingCard(self.twitCard)
        self.searchGroup.addSettingCard(self.hotCard)
        self.searchGroup.addSettingCard(self.apiCard)
        self.searchGroup.addSettingCard(self.loginCard)
        self.searchGroup.addSettingCard(self.levelCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.DownloadSettings)
        self.expandLayout.addWidget(self.searchGroup)
        self.expandLayout.addWidget(self.personalGroup)
        if cfg.beta.value:
            self.expandLayout.addWidget(self.BetaOnlyGroup)
        self.expandLayout.addWidget(self.appGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return
        cfg.set(cfg.downloadFolder, folder)
        self.LabelFolder.setText(f"\n    当前路径为：{folder}\n")
        ref(musicpath=folder)
        setOK(parent=self.window())
        
    def __FolederAutoCardClicked(self):
        cfg.set(cfg.downloadFolder, autopath)
        self.LabelFolder.setText(f"\n    当前路径为：{autopath}\n")
        ref(musicpath=autopath)
        setOK(parent=self.window())
        
    def __customapis(self):
        w = editapi(parent=self.window(), ncmaapi=cfg.ncma_api.value, qqmaapi=cfg.qqma_api.value)
        if w:
            cfg.set(cfg.ncma_api, w[0])
            cfg.set(cfg.qqma_api, w[1])
            setOK(parent=self.window())
        
    def __backtoinitClicked(self):
        w = DeleteAllData(self.window())
        if not w.exec():
            delfin(IfMusicPath=w.DataCheckBox.isChecked())
            exit(0)

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)

        # chang the theme of setting interface
        setSettingsQss(parent=self)
        setOK(parent=self.window())
        
    def beta_not(self):
        if not cfg.beta.value:
            self.debug_Card.setValue(False)
            self.plugin_Card.setValue(False)
            self.toast_Card.setValue(False)
            self.debug_Card.setVisible(False)
            self.plugin_Card.setVisible(False)
            self.toast_Card.setVisible(False)
            self.BetaOnlyGroup.setVisible(False)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(lambda: restart(parent=self.window()))
        pfg.appRestartSig.connect(lambda: restart(parent=self.window()))
        cfg.themeChanged.connect(self.__onThemeChanged)
        pfg.themeChanged.connect(self.__onThemeChanged)
        self.micaCard.checkedChanged.connect(self.micaEnableChanged)
        self.AutoFolder.clicked.connect(self.__FolederAutoCardClicked)
        self.changeFolder.clicked.connect(self.__onDownloadFolderCardClicked)
        self.backtoinit.clicked.connect(self.__backtoinitClicked)
        self.beta.checkedChanged.connect(self.beta_not)
        self.aboutCard.clicked.connect(lambda: changelog(parent=self))
        self.feedbackCard.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
        self.ApiUrlCard.clicked.connect(self.__customapis)
    def showMessage(self):
        global ms_login_data
        w = LoginMessageBox(self.window())
        if w.exec():
            w.stop()
