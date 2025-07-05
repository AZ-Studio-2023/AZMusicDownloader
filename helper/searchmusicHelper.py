# coding: utf-8
import AZMusicAPI
import json

import os
import requests
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QTableWidgetItem, QCompleter

import helper.config
from helper.config import cfg, pfg
from helper.flyoutmsg import dlerr, dlwar
from helper.getvalue import searchSong, set_download_search_song
from helper.inital import mkf
from helper.loggerHelper import logger
from helper.pluginHelper import plugins_api_items

api = cfg.ncma_api.value
q_api = cfg.qqma_api.value
mkf()


def is_english_and_characters(input_string):
    return all(char.isalpha() or not char.isspace() for char in input_string)


class getlist(QThread):
    finished = pyqtSignal()

    @pyqtSlot()
    def run(self):
        data = searchSong
        text = data["text"]
        value = data["value"]
        api_value = data["api_value"]
        keywords = text

        if pfg.apicard.value == "NCMA":
            self.songInfos = AZMusicAPI.getmusic(keywords, number=value, api=api_value, cookie=cfg.cookie.value)
        elif pfg.apicard.value == "QQMA":
            self.songInfos = AZMusicAPI.getmusic(keywords, number=value, api=api_value, server="qqma")
        elif pfg.apicard.value == "Bilibili":
            self.songInfos = AZMusicAPI.getmusic(keywords, number=value, api="", server="bili")
        else:
            try:
                api_plugin = plugins_api_items[pfg.apicard.value]
                self.songInfos = api_plugin.getmusic(keyword=keywords, number=value)
            except Exception as e:
                if cfg.debug_card.value:
                    logger.error(f"插件错误：{e}")
                self.songInfos = "PluginAPIImportError"
        self.finished.emit()


def sethotlineEdit(lineEdit):
    if helper.config.cfg.hotcard.value:
        try:
            data = requests.get(api + "search/hot").json()["result"]["hots"]
            hot_song = []
            for i in data:
                hot_song.append(i["first"])
            completer = QCompleter(hot_song, lineEdit)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setMaxVisibleItems(10)
            lineEdit.setCompleter(completer)
        except:
            pass


def searchstart(lineEdit, parent, spinBox, lworker, progressbar):
    global searchSong
    if pfg.apicard.value == "NCMA":
        if api == "" or api is None:
            dlerr(outid=4, parent=parent)
            return "Error"
        searchSong = {"text": lineEdit.text(), "api_value": api, "value": spinBox.value()}
    elif pfg.apicard.value == "QQMA":
        if q_api == "" or q_api is None:
            dlerr(outid=5, parent=parent)
            return "Error"
        searchSong = {"text": lineEdit.text(), "api_value": q_api, "value": spinBox.value()}
    else:
        searchSong = {"text": lineEdit.text(), "api_value": "", "value": spinBox.value()}
    progressbar.setHidden(False)
    lworker.start()


def rundownload(primaryButton1, ProgressBar, tableView, parent, dworker, lworker):
    global download_search_song
    musicpath = cfg.get(cfg.downloadFolder)
    primaryButton1.setEnabled(False)
    ProgressBar.setHidden(False)
    ProgressBar.setValue(0)

    row = tableView.currentIndex().row()
    if "Error" in lworker.songInfos:
        dlwar(3, parent=parent)
        return 0
    try:
        songdata = lworker.songInfos
        data = songdata[row]
    except:
        dlwar(3, parent=parent)
        return 0

    song_id = data["id"]
    song = data["name"]
    singer = data["artists"]

    try:
        if os.path.exists(musicpath) == False:
            os.mkdir(musicpath)
    except:
        dlerr(outid=3, parent=parent)
        return 0

    # self.dworker.started.connect(lambda: self.dworker.run(id=song_id, api=api, song=song, singer=singer))
    if pfg.apicard.value == "NCMA":
        if api == "" or api is None:
            dlerr(outid=4, parent=parent)
            return "Error"
        download_search_song = {"id": song_id, "api": api, "song": song, "singer": singer}
    elif pfg.apicard.value == "QQMA":
        if q_api == "" or q_api is None:
            dlerr(outid=5, parent=parent)
            return "Error"
        download_search_song = {"id": song_id, "api": q_api, "song": song, "singer": singer}
    else:
        download_search_song = {"id": song_id, "song": song, "singer": singer}
    set_download_search_song(value=download_search_song)
    dworker.start()


def search(lworker, parent, tableView, spinBox, progressbar):
    songInfos = lworker.songInfos
    progressbar.setHidden(True)
    if songInfos == "Error 0":
        dlwar(outid=0, parent=parent)
        return 0
    elif songInfos == "Error 1":
        dlwar(outid=1, parent=parent)
        return 0
    elif songInfos == "NetworkError":
        dlerr(outid=6, parent=parent)
        return 0
    elif songInfos == "PluginAPIImportError":
        dlerr(9, parent)
        return 0
    tableView.setRowCount(spinBox.value())
    for i in range(len(songInfos)):
        data = songInfos[i]
        num = i + 1
        song_id = data["id"]
        title = data["name"]
        Artist = data["artists"]
        Album = data["album"]

        # if len(title) > 8:
        #     title = title[:8] + "..."
        # if len(Artist) > 8:
        #     Artist = Artist[:8] + "..."
        # if len(Album) > 8:
        #     Album = Album[:8] + "..."

        data = []
        data.append(str(song_id))
        data.append(title)
        data.append(Artist)
        data.append(Album)
        for j in range(4):
            tableView.setItem(i, j, QTableWidgetItem(data[j]))

    tableView.resizeColumnsToContents()
    lworker.quit()