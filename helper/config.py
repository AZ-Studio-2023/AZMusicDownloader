# coding:utf-8
from enum import Enum
from sys import platform, getwindowsversion
from helper.getvalue import configpath, autopath
from PyQt5.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator,  FolderValidator, ConfigSerializer)

class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    # Folders
    downloadFolder = ConfigItem(
        "Folders", "Download", autopath, FolderValidator())

    # Application
    beta = ConfigItem(
        "Application", "beta", False, BoolValidator(), restart=True)
    update_card = ConfigItem(
        "Application", "update_card", False, BoolValidator(), restart=True)
    debug_card = ConfigItem(
        "Application", "debug_card", False, BoolValidator(), restart=True)
    
    # Search
    twitcard = ConfigItem(
        "Search", "twitcard", False, BoolValidator(), restart=True)
    hotcard = ConfigItem(
        "Search", "hotcard", False, BoolValidator(), restart=True)
    apicard = OptionsConfigItem(
        "Search", "apicard", "NCMA", OptionsValidator(['NCMA', 'QQMA']))
    
    # Personalize
    language = OptionsConfigItem(
        "Personalize", "Language", Language.CHINESE_SIMPLIFIED, OptionsValidator(Language), LanguageSerializer(), restart=True)
    micaEnabled = ConfigItem("Personalize", "MicaEnabled", platform == 'win32' and getwindowsversion().build >= 22000, BoolValidator())

cfg = Config()
qconfig.load(configpath, cfg)