import json
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QTableWidgetItem

from PyQt5.QtCore import pyqtSignal, pyqtSlot
import os
import requests
from helper.config import cfg
from helper.getvalue import playlist_search_log, playlist_download_log, autoncmaapi, playlistpath
from helper.flyoutmsg import dlerr, dlwar

api = cfg.ncma_api.value

class getlist(QThread):
    finished = pyqtSignal()

    @pyqtSlot()
    def run(self):
        u = open(playlist_search_log, "r")
        data = json.loads(u.read())
        u.close()
        type_value = data["type_value"]
        value = data["value"]
        api_value = data["api_value"]
        value = data["value"]
        api_value = data["api_value"]
        keywords = value
        if type_value == "用户":
            api_v = api_value + "user/playlist"
            params = {"uid": str(value)}
            data = requests.get(api_v, params=params).json()
            data = data["playlist"]
            for playlist in data:
                id_v = playlist["id"]
                api_v = api_value + "playlist/detail"
                params = {"id": id_v}
                data_y = requests.get(api_v, params=params).json()
                data = data_y["playlist"]
                if data_y["code"] != 400:
                    name = data["name"]
                    data = data["tracks"]
                    if not os.path.isdir(playlistpath + "\\" + name):
                        os.mkdir("{}\\{}".format(playlistpath, name))
                        data_v = []
                        try:
                            for i in range(len(data)):
                                artists = ""
                                for y in range(len(data[i]["ar"])):
                                    if y != 0:
                                        artists = artists + ","
                                    artists = artists + data[i]["ar"][y]["name"]
                                data_v.append({"id": data[i]['id'], "name": data[i]['name'], "artists": artists,
                                               "album": data[i]['al']["name"]})
                        except:
                            data_v.append({"id": '-1', "name": 'error', "artists": 'error',
                                           "album": 'error'})
                        u = open("{}\\{}\\index.json".format(playlistpath, name), "w")
                        u.write(json.dumps({"content": data_v}))
                        u.close()
        else:
            id_v = value
            api_v = api_value + "playlist/detail"
            params = {"id": id_v}
            data_y = requests.get(api_v, params=params).json()
            data = data_y["playlist"]

            if data_y["code"] == 200:
                name = data["name"]
                data = data["tracks"]
                if not os.path.exists("{}\\{}".format(playlistpath, name)):
                    os.mkdir("{}\\{}".format(playlistpath, name))
                    data_v = []

                    try:
                        for i in range(len(data)):
                            artists = ""
                            for y in range(len(data[i]["ar"])):
                                if y != 0:
                                    artists = artists + ","
                                artists = artists + data[i]["ar"][y]["name"]
                            data_v.append({"id": data[i]['id'], "name": data[i]['name'], "artists": artists,
                                           "album": data[i]['al']["name"]})
                    except:
                        data_v.append({"id": '-1', "name": 'error', "artists": 'error',
                                       "album": 'error'})

                    u = open("{}\\{}\\index.json".format(playlistpath, name), "w")
                    u.write(json.dumps({"content": data_v}))
                    u.close()
        self.finished.emit()


def FindLists(TableWidget):
    data = get_folders(playlistpath)
    TableWidget.setRowCount(len(data))
    TableWidget.clearContents()

    for i in range(len(data)):
        data_v = []
        data_v.append(str(i + 1))
        data_v.append(data[i])
        for j in range(2):
            TableWidget.setItem(i, j, QTableWidgetItem(data_v[j]))


def searchstart(PushButton, lworker, ComboBox, LineEdit, parent):
    if LineEdit.text() != '':
        PushButton.setEnabled(False)
        # self.getlist_worker.started.connect(
        #     lambda: self.lworker.run(type_value=self.ComboBox.text(), value=self.LineEdit.text(), api_value=api))
        u = open(playlist_search_log, "w")
        u.write(json.dumps({"type_value": ComboBox.text(), "value": LineEdit.text(), "api_value": api}))
        u.close()
        lworker.start()
    else:
        dlerr(outid=1, parent=parent)


def music(TableWidget, TableWidget_2, Button, parent):
    try:
        name = get_folders(playlistpath)[TableWidget.currentIndex().row()]
        u = open("{}\\{}\\index.json".format(playlistpath, name), "r")
        data = json.loads(u.read())
        u.close()
        data = data["content"]
        TableWidget_2.clearContents()
        TableWidget_2.setRowCount(len(data))

        #All = []
        for i in range(len(data)):
            #add = []
            id_v = str(data[i]["id"])
            name_v = str(data[i]["name"])
            artists_v = str(data[i]["artists"])
            album_v = str(data[i]["album"])
            
            TableWidget_2.setItem(i, 0, QTableWidgetItem(id_v))
            TableWidget_2.setItem(i, 1, QTableWidgetItem(name_v))
            TableWidget_2.setItem(i, 2, QTableWidgetItem(artists_v))
            TableWidget_2.setItem(i, 3, QTableWidgetItem(album_v))
            
        TableWidget_2.resizeColumnsToContents()
        Button.setText(name)
    except:
        dlerr(erid=2, parent=parent)


def search(lworker, TableWidget):
    data = get_folders(playlistpath)
    TableWidget.setRowCount(len(data))
    TableWidget.clearContents()

    for i in range(len(data)):
        data_v = []
        data_v.append(str(i + 1))
        data_v.append(data[i])
        for j in range(2):
            TableWidget.setItem(i, j, QTableWidgetItem(data_v[j]))

    TableWidget.resizeColumnsToContents()
    lworker.quit()


def rundownload(PushButton_2, pro_bar, TableWidget_2, parent, dworker):
    PushButton_2.setEnabled(False)
    pro_bar.setValue(0)
    pro_bar.setHidden(False)

    try:
        row = TableWidget_2.currentIndex().row()
        id_v = str(TableWidget_2.item(row, 0).text())
    except AttributeError:
        TableWidget_2.clearSelection()
        PushButton_2.setEnabled(False)
        dlwar(outid=2, parent=parent)
        pro_bar.setHidden(True)
        return 0

    if id_v != "":
        song_id = id_v
        song = str(TableWidget_2.item(row, 1).text())
        singer = str(TableWidget_2.item(row, 2).text())
        album = str(TableWidget_2.item(row, 3).text())

        try:
            if os.path.exists(cfg.get(cfg.downloadFolder)) == False:
                os.mkdir(cfg.get(cfg.downloadFolder))
        except:
            dlerr(outid=3, parent=parent)
            return 0

        # self.download_worker.started.connect(
        #     lambda: self.dworker.run(id=song_id, api=api, song=song, singer=singer))
        u = open(playlist_download_log, 'w')
        u.write(json.dumps({"id": song_id, "api": api, "song": song, "singer": singer, "album": album}))
        u.close()
        dworker.start()
    else:
        TableWidget_2.clearSelection()
        PushButton_2.setEnabled(False)
        dlwar(outid=2, parent=parent)


def get_folders(folder_path):
    folders = []

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            folders.append(item)

    return folders

