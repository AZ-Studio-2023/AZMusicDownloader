import json, requests, webbrowser
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from os import path, makedirs, remove
from json import loads
from helper.flyoutmsg import dlsuc, dlwar, flyout_bottom
from helper.getvalue import outapoem
from PyQt5.QtCore import QThread
from helper.config import cfg
from qfluentwidgets import isDarkTheme
from helper.getvalue import (download_log, search_log, configpath, upurl, VERSION,
                             playlistpath, logpath, playlist_download_log, playlist_search_log, UPDATE_ORDER)


# 初始化创建文件
def mkf():
    dlpath = cfg.get(cfg.downloadFolder)
    if not path.exists(logpath):
        makedirs(logpath)
    if not path.exists(download_log):
        d = open(download_log, "w")
        d.close()
    if not path.exists(playlist_download_log):
        d = open(playlist_download_log, "w")
        d.close()
    if not path.exists(playlist_search_log):
        d = open(playlist_search_log, "w")
        d.close()
    if not path.exists(search_log):
        d = open(search_log, "w")
        d.close()
    if not path.exists(dlpath):
        makedirs(dlpath)
    if not path.exists(playlistpath):
        makedirs(playlistpath)


# 删除用户数据
def delfin(IfMusicPath=False):
    if path.exists(configpath):
        remove(configpath)
    if path.exists(playlist_download_log):
        remove(playlist_download_log)
    if path.exists(playlist_search_log):
        remove(playlist_search_log)
    if path.exists(download_log):
        remove(download_log)
    if path.exists(search_log):
        remove(search_log)
    if IfMusicPath:
        downloadFolder = cfg.get(cfg.downloadFolder)
        if path.exists(downloadFolder):
            remove(downloadFolder)


# 检查更新
def getup():
    url = upurl
    try:
        ud = requests.get(url).text
        data = loads(ud)
        msg = data
    except:
        poem = "在等待的过程中，来读句古诗词吧：" + outapoem()
        ud = {"latest": "0.0.0", "title": "(⊙o⊙)？",
              "text": "呀！获取不到更新数据了 ＞﹏＜ 请检查您的网络连接\n{}".format(poem), "time": 200000,
              "button": "（；´д｀）ゞ", "link": "https://azstudio.net.cn"}
        msg = ud
    return msg


class get_update(QThread):
    finished = pyqtSignal(dict)

    @pyqtSlot()
    def run(self):
        data = getup()
        self.finished.emit(data)


def showup(parent, updata, upworker):
    up = updata
    if not VERSION == up["latest"] and up["latest"] != "0.0.0":
        if UPDATE_ORDER < up["update_order"]:
            # 等级可为：normal（普通的），important（重要的），fix（修复版），special（特殊意义版）
            if up["level"] == "normal":
                text = "我们检测到了新的版本，版本号：{}\n本次更新为日常版本迭代，更新了新功能，可选择性进行更新。".format(
                    str(up["latest"]))
                dlwar("检测到有新版本 {} ，本次更新为日常版本迭代，可选择进行更新。".format(str(up["latest"])),
                      parent, title="更新提示", show_time=up["flag_time"])
            elif up["level"] == "important":
                text = "我们检测到了新的版本，版本号：{}\n本次更新为重要版本迭代，修复了Bug，更新了新功能，强烈建议进行更新。".format(
                    str(up["latest"]))
                dlwar("检测到有新版本 {} ，本次更新为重要版本迭代，强烈建议进行更新。".format(str(up["latest"])),
                      parent, title="更新提示", show_time=up["flag_time"])
            elif up["level"] == "fix":
                text = "我们检测到了新的版本，版本号：{}\n本次更新为Bug修复版本，修复了重大Bug，强烈建议进行更新。".format(
                    str(up["latest"]))
                dlwar("检测到有新版本 {} ，本次更新为Bug修复版本，强烈建议进行更新。".format(str(up["latest"])),
                      parent, title="更新提示", show_time=up["flag_time"])
            elif up["level"] == "special":
                text = "我们检测到了新的版本，版本号：{}\n{}".format(
                    str(up["latest"]), up["special"])
                dlwar("检测到有新版本 {} \n{}".format(str(up["latest"]), up["special"]),
                      parent, title="更新提示", show_time=up["flag_time"])
            else:
                text = "我们检测到了新的版本，版本号：{}\n本次更新类型未知，可能是后续版本的新更新类型。".format(
                    str(up["latest"]))
                dlwar("检测到有新版本 {} ，本次更新类型未知，可能是后续版本的新更新类型。".format(str(up["latest"])),
                      parent, title="更新提示", show_time=up["flag_time"])
            flyout_bottom(parent=parent, title="有新版本可用", content=text, button_content=up["button"],
                          button_todo=lambda: webbrowser.open_new_tab(up["link"]), duration=up["time"])
        elif UPDATE_ORDER > up["update_order"]:
            dlsuc(content="您正在使用测试版本", parent=parent, title="提示", show_time=5000)
        else:
            dlsuc(content="您使用的版本是最新版本", parent=parent, title="恭喜", show_time=5000)
    elif up["latest"] == "0.0.0":
        flyout_bottom(parent=parent, title=up["title"], content=up["text"], button_content=up["button"],
                      button_todo=lambda: webbrowser.open_new_tab(up["link"]), duration=up["time"])
    else:
        dlsuc(content="您使用的版本是最新版本", parent=parent, title="恭喜", show_time=5000)
    upworker.quit()


# qss设置
def setSettingsQss(parent, which="setting_interface"):
    theme = 'dark' if isDarkTheme() else 'light'
    with open(f'resource/qss/{theme}/{which}.qss', encoding='utf-8') as f:
        parent.setStyleSheet(f.read())
