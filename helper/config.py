# coding:utf-8
from enum import Enum
import datetime
import winreg

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QGuiApplication, QFont
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            ColorConfigItem, OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator, ConfigSerializer, __version__)


class SongQuality(Enum):
    """ Online song quality enumeration class """

    STANDARD = "Standard quality"
    HIGH = "High quality"
    SUPER = "Super quality"
    LOSSLESS = "Lossless quality"


class MvQuality(Enum):
    """ MV quality enumeration class """

    FULL_HD = "Full HD"
    HD = "HD"
    SD = "SD"
    LD = "LD"


# class Language(Enum):
#     """ Language enumeration """

#     CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
#     CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
#     ENGLISH = QLocale(QLocale.English)
#     AUTO = QLocale()


# class LanguageSerializer(ConfigSerializer):
#     """ Language serializer """

#     def serialize(self, language):
#         return language.value.name() if language != Language.AUTO else "Auto"

#     def deserialize(self, value: str):
#         return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    """ Config of application """

    # folders
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    documents_path_value = winreg.QueryValueEx(reg_key, "My Music")
    personalmusicpath = documents_path_value[0]
    autopath = "{}\\AZMusicDownload".format(personalmusicpath)
    downloadFolder = ConfigItem(
        "Folders", "Download", autopath, FolderValidator())

    # main window
    beta = ConfigItem(
        "MainWindow", "beta", False, BoolValidator(), restart=True)
    adcard = ConfigItem(
        "MainWindow", "adcard", False, BoolValidator(), restart=True)
    twitcard = ConfigItem(
        "MainWindow", "twitcard", False, BoolValidator(), restart=True)
    hotcard = ConfigItem(
        "MainWindow", "hotcard", False, BoolValidator(), restart=True)
    playBarColor = ColorConfigItem("MainWindow", "PlayBarColor", "#225C7F")
    recentPlaysNumber = RangeConfigItem(
        "MainWindow", "RecentPlayNumbers", 300, RangeValidator(10, 300))
    # language = OptionsConfigItem(
    #     "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)
    
    @property
    def desktopLyricFont(self):
        """ get the desktop lyric font """
        font = QFont(self.deskLyricFontFamily.value)
        font.setPixelSize(self.deskLyricFontSize.value)
        return font

    @desktopLyricFont.setter
    def desktopLyricFont(self, font: QFont):
        dpi = QGuiApplication.primaryScreen().logicalDotsPerInch()
        self.deskLyricFontFamily.value = font.family()
        self.deskLyricFontSize.value = max(15, int(font.pointSize()*dpi/72))
        self.save()

YEAR = int(datetime.date.today().year)
AUTHOR = "AZ Studio"
VERSION = "2.2.0"
HELP_URL = "https://azstudio.net.cn/"
FEEDBACK_URL = "https://azstudio.net.cn/"
RELEASE_URL = "https://azstudio.net.cn/"


cfg = Config()
qconfig.load('config/config.json', cfg)