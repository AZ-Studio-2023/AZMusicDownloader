import json
import os
import sys
from helper.inital import setSettingsQss
from PyQt5.QtCore import Qt, QPoint, QSize, QUrl, QRect, QStandardPaths
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy
from helper.config import cfg
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, CustomColorSettingCard,
                            OptionsSettingCard, FolderListSettingCard, PushSettingCard, setTheme, isDarkTheme,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea, PushButton, PrimaryPushButton,
                            ComboBoxSettingCard, ExpandLayout, Theme, InfoBar, FlyoutView, Flyout)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets.components.widgets.acrylic_label import AcrylicBrush
from helper.pluginHelper import run_plugins_plugin
import window.main

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
        self.ListsGroup.addSettingCard(self.PluginListCard)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.ListsGroup)
        self.expandLayout.addWidget(self.PluginsGroup)
            
        
