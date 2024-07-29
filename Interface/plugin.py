import json
import os
import sys
from helper.inital import setSettingsQss
from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtWidgets import QWidget
from helper.config import cfg
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import SettingCardGroup, FolderListSettingCard, ScrollArea, ExpandLayout, HyperlinkCard
from helper.pluginHelper import run_plugins_plugin
from helper.getvalue import PLU_URL

class plugins(ScrollArea):

    def __init__(self):
        super().__init__()
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.setObjectName('plugins')
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 20, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.scrollWidget.setObjectName('scrollWidget')
        
        self.ListsGroup = SettingCardGroup(self.tr('已导入的插件'), self.scrollWidget)
        self.PluginsGroup = SettingCardGroup(self.tr('管理插件'), self.scrollWidget)
        run_plugins_plugin(parent=self, PluginsGroup=self.PluginsGroup)
        setSettingsQss(parent=self)
        
        self.PluginListCard = FolderListSettingCard(
            cfg.PluginFolders,
            "插件",
            directory=QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
            parent=self.ListsGroup
        )
        self.StoreCard = HyperlinkCard(
            PLU_URL,
            self.tr('浏览器打开'),
            FIF.TAG,
            self.tr('插件商店'),
            self.tr('AZ Studio制作的AZMusicDownloader官方插件商店（暂未上线）'),
            self.ListsGroup
        )
        self.StoreCard.setEnabled(False)
        
        self.ListsGroup.addSettingCard(self.PluginListCard)
        self.ListsGroup.addSettingCard(self.StoreCard)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.ListsGroup)
        self.expandLayout.addWidget(self.PluginsGroup)
            
        
