# coding:utf-8
import importlib
import json
import os

from Interface.searchmusic import searchmusic
from Interface.settings import SettingInterface

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import NavigationItemPosition, MSFluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF
from Interface.localmusics import localmusics
from Interface.playlist import playlist
from helper.config import Config
from Interface.plugin import plugins
from helper.config import cfg
from helper.getvalue import apipath, autoapi

try:
    u = open(apipath, "r")
    data = json.loads(u.read())
    api = data["api"]
    q_api = data["q_api"]
    u.close()
except:
    api = autoapi
    q_api = ""

# Print logs | 日志输出
if cfg.debug_card.value:
    print("————————日志信息————————")
    if Config.beta.value:
        print("Beta实验功能：启用")
    else:
        print("Beta实验功能：禁用")
    if cfg.debug_card.value:
        print("Debug模式：启用")
    else:
        print("Debug模式：禁用")
    print("使用的NeteaseCloudMusicApi：" + api)
    print("使用的QQMusicApi：" + q_api)
    print("选择的API："+cfg.apicard.value)
    print(f"显示语言：{Config.language.value}")

if not os.path.exists("plugins"):
    os.mkdir("plugins")


def get_folders(directory):
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folders.append(item)
    return folders


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.initNavigation()
        self.initWindow()

    def load_plugins(self):
        # 遍历插件目录中的文件
        self.plugin_dir = "plugins"
        self.plugins = {}
        num = 0
        if cfg.debug_card.value:
            print("————————插件导入————————")
        for dirname in get_folders(self.plugin_dir):
            for filename in os.listdir(f'plugins\\{dirname}'):
                if filename.endswith('.py'):
                    plugin_name = filename[:-3]
                    module_name = f"{self.plugin_dir}.{dirname}.{plugin_name}"
                    try:
                        module = importlib.import_module(module_name)
                        plugin_class = getattr(module, plugin_name.capitalize())
                        self.plugins[plugin_name] = plugin_class()
                        if cfg.debug_card.value:
                            print(f"导入插件: {plugin_name}")
                        num = num + 1
                    except Exception as e:
                        if cfg.debug_card.value:
                            print(f"导入{plugin_name}插件错误: {e}")
        if cfg.debug_card.value:
            print(f"成功导入了{str(num)}个插件")

    def run_plugins(self):
        for plugin_name, plugin_instance in self.plugins.items():
            get_v = open(f"plugins/{plugin_name}/index.json", "r", encoding="utf-8")
            data = json.loads(get_v.read())
            get_v.close()
            if bool(data["nav"]):
                icon = data["show_icon"]
                name = data["name"]
                if cfg.debug_card.value:
                    print(f"将插件添加至导航栏: {plugin_name}")
                exec(f"self.addSubInterface(plugin_instance, {icon}, '{name}')")

    def initNavigation(self):
        self.addSubInterface(searchmusic(), FIF.CARE_RIGHT_SOLID, '搜索下载')
        self.addSubInterface(localmusics(), FIF.MUSIC_FOLDER, '我的音乐库')
        if Config.beta.value:
            self.addSubInterface(playlist(), FIF.EXPRESSIVE_INPUT_ENTRY, '歌单')
            self.addSubInterface(plugins(), FIF.BOOK_SHELF, '插件', position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(SettingInterface(), FIF.SETTING, '设置', position=NavigationItemPosition.BOTTOM)
        if Config.beta.value:
            self.load_plugins()
            self.run_plugins()

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('AZMusicDownloader')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
