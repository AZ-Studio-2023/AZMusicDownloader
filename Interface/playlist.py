import json
import AZMusicAPI
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QWidget, QAbstractItemView, QHBoxLayout
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtWidgets
import win32api, win32con
import os
import requests
from mutagen.easyid3 import EasyID3
from helper.config import cfg

try:
    u = open("api.json", "r")
    data = json.loads(u.read())
    api = data["api"]
    u.close()
except:
    api = "https://ncma.zenglingkun.cn/"

if not os.path.isdir("playlist"):
    os.mkdir("playlist")


class downloading(QThread):
    finished = pyqtSignal(str)

    @pyqtSlot()
    def run(self):
        musicpath = cfg.get(cfg.downloadFolder)
        u = open("log\\list_download.json", "r")
        data = json.loads(u.read())
        u.close()
        id = data["id"]
        api = data["api"]
        song = data["song"]
        singer = data["singer"]
        url = AZMusicAPI.geturl(id=id, api=api)
        if url == "Error 3":
            win32api.MessageBox(0, '这首歌曲无版权，暂不支持下载', '错误', win32con.MB_ICONWARNING)
            return 0
        elif url == "NetworkError":
            win32api.MessageBox(0, '您可能是遇到了以下其一问题：网络错误 / 服务器宕机 / IP被封禁', '错误',
                                win32con.MB_ICONWARNING)
            return 0
        response = requests.get(url, stream=True)
        file_size = int(response.headers.get('content-length', 0))
        chunk_size = file_size // 100
        path = "{}\\{} - {}.mp3".format(musicpath, singer, song)
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                downloaded_bytes = f.tell()
                progress = downloaded_bytes * 100 // file_size
                if downloaded_bytes % chunk_size == 0:
                    self.finished.emit(str(progress))

        self.finished.emit(str(200))


class getlist(QThread):
    finished = pyqtSignal()

    @pyqtSlot()
    def run(self):
        u = open("log\\list_search.json", "r")
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
                    if not os.path.isdir("playlist\\" + name):
                        os.mkdir("playlist\\{}".format(name))
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
                        u = open("playlist\\{}\\index.json".format(name), "w")
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
                if not os.path.exists("playlist\\{}".format(name)):
                    os.mkdir("playlist\\{}".format(name))
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
                    u = open("playlist\\{}\\index.json".format(name), "w")
                    u.write(json.dumps({"content": data_v}))
                    u.close()
        self.finished.emit()


class playlist(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('playlist')
        self.resize(948, 623)
        self.SubtitleLabel = SubtitleLabel(self)
        self.SubtitleLabel.setGeometry(QtCore.QRect(390, 170, 119, 28))
        self.SubtitleLabel.setObjectName("SubtitleLabel")
        self.ComboBox = ComboBox(self)
        self.ComboBox.setGeometry(QtCore.QRect(425, 230, 111, 32))
        self.ComboBox.setObjectName("ComboBox")
        self.SubtitleLabel_2 = SubtitleLabel(self)
        self.SubtitleLabel_2.setGeometry(QtCore.QRect(320, 230, 119, 28))
        self.SubtitleLabel_2.setObjectName("SubtitleLabel_2")
        self.SubtitleLabel_3 = SubtitleLabel(self)
        self.SubtitleLabel_3.setGeometry(QtCore.QRect(340, 280, 119, 28))
        self.SubtitleLabel_3.setObjectName("SubtitleLabel_3")
        self.LineEdit = LineEdit(self)
        self.LineEdit.setGeometry(QtCore.QRect(425, 280, 111, 33))
        self.LineEdit.setObjectName("LineEdit")
        self.PushButton = PushButton(self)
        self.PushButton.setGeometry(QtCore.QRect(380, 330, 102, 32))
        self.PushButton.setObjectName("PushButton")
        self.PushButton.clicked.connect(self.searchstart)
        self.TableWidget = TableWidget(self)
        self.TableWidget.setGeometry(QtCore.QRect(15, 11, 281, 601))
        self.TableWidget.setObjectName("TableWidget")
        self.TableWidget.setWordWrap(False)
        self.TableWidget.setRowCount(30)
        self.TableWidget.setColumnCount(2)
        self.TableWidget.verticalHeader().hide()
        self.TableWidget.setHorizontalHeaderLabels(['序号', '歌单'])
        self.TableWidget.cellDoubleClicked.connect(self.music)
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TableWidget_2 = TableWidget(self)
        self.TableWidget_2.setGeometry(QtCore.QRect(540, 0, 391, 611))
        self.TableWidget_2.setObjectName("TableWidget_2")
        self.TableWidget_2.setColumnCount(0)
        self.TableWidget_2.setRowCount(0)
        self.TableWidget_2.setWordWrap(False)
        self.TableWidget_2.setRowCount(30)
        self.TableWidget_2.setColumnCount(4)
        self.TableWidget_2.verticalHeader().hide()
        self.TableWidget_2.setHorizontalHeaderLabels(['ID', '歌曲名', '艺术家', '专辑'])
        self.TableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TableWidget_2.itemSelectionChanged.connect(self.openbutton)
        self.PushButton_2 = PushButton(self)
        self.PushButton_2.setGeometry(QtCore.QRect(380, 370, 102, 32))
        self.PushButton_2.setObjectName("PushButton_2")
        self.PushButton_2.clicked.connect(self.rundownload)
        self.pro_bar = ProgressBar(self)
        self.pro_bar.setGeometry(QtCore.QRect(380, 410, 102, 32))
        self.pro_bar.setHidden(True)
        self.pro_bar.setMaximum(100)
        self.retranslateUi()
        self.lworker = getlist()
        self.lworker.finished.connect(self.search)
        self.dworker = downloading()
        self.dworker.finished.connect(self.download)
        data = get_folders("playlist")
        self.TableWidget.setRowCount(len(data))
        self.TableWidget.clearContents()
        for i in range(len(data)):
            data_v = []
            data_v.append(str(i + 1))
            data_v.append(data[i])
            for j in range(2):
                self.TableWidget.setItem(i, j, QTableWidgetItem(data_v[j]))
        self.TableWidget.resizeColumnsToContents()
        QtCore.QMetaObject.connectSlotsByName(self)

    def openbutton(self):
        self.PushButton_2.setEnabled(True)

    @pyqtSlot()
    def searchstart(self):
        self.PushButton.setEnabled(False)
        # self.getlist_worker.started.connect(
        #     lambda: self.lworker.run(type_value=self.ComboBox.text(), value=self.LineEdit.text(), api_value=api))
        u = open("log\\list_search.json", "w")
        u.write(json.dumps({"type_value": self.ComboBox.text(), "value": self.LineEdit.text(), "api_value": api}))
        u.close()
        self.lworker.start()

    def music(self):
        try:
            name = get_folders("playlist")[self.TableWidget.currentIndex().row()]
            u = open("playlist\\{}\\index.json".format(name), "r")
            data = json.loads(u.read())
            u.close()
            data = data["content"]
            self.TableWidget_2.clearContents()
            for i in range(len(data)):
                add = []
                id_v = str(data[i]["id"])
                name_v = str(data[i]["name"])
                artists_v = str(data[i]["artists"])
                album_v = str(data[i]["album"])
                add.append(id_v)
                add.append(name_v)
                add.append(artists_v)
                add.append(album_v)
                for j in range(4):
                    self.TableWidget_2.setItem(i, j, QTableWidgetItem(add[j]))
            self.TableWidget_2.resizeColumnsToContents()
            self.TableWidget_2.setRowCount(len(data))
        except:
            win32api.MessageBox(0, '您双击的行无数据', '错误', win32con.MB_ICONWARNING)

    @pyqtSlot()
    def search(self):
        data = get_folders("playlist")
        self.TableWidget.setRowCount(len(data))
        self.TableWidget.clearContents()
        for i in range(len(data)):
            data_v = []
            data_v.append(str(i + 1))
            data_v.append(data[i])
            for j in range(2):
                self.TableWidget.setItem(i, j, QTableWidgetItem(data_v[j]))
        self.TableWidget.resizeColumnsToContents()
        self.PushButton.setEnabled(True)
        self.lworker.quit()

    @pyqtSlot()
    def rundownload(self):
        self.PushButton_2.setEnabled(False)
        self.pro_bar.setValue(0)
        self.pro_bar.setHidden(False)
        row = self.TableWidget_2.currentIndex().row()
        id_v = str(self.TableWidget_2.item(row, 0).text())
        if id_v != "":
            song_id = id_v
            song = str(self.TableWidget_2.item(row, 1).text())
            singer = str(self.TableWidget_2.item(row, 2).text())
            album = str(self.TableWidget_2.item(row, 3).text())
            try:
                if os.path.exists(cfg.get(cfg.downloadFolder)) == False:
                    os.mkdir(cfg.get(cfg.downloadFolder))
            except:
                win32api.MessageBox(0, '音乐下载路径无法读取\创建失败', '错误', win32con.MB_ICONWARNING)
                return 0
            # self.download_worker.started.connect(
            #     lambda: self.dworker.run(id=song_id, api=api, song=song, singer=singer))
            if not os.path.exists("log"):
                os.mkdir("log")
            u = open("log\\list_download.json", 'w')
            u.write(json.dumps({"id": song_id, "api": api, "song": song, "singer": singer, "album": album}))
            u.close()
            self.dworker.start()
        else:
            self.TableWidget_2.clearSelection()
            self.PushButton_2.setEnabled(False)
            win32api.MessageBox(0, '您选中的行无数据', '错误', win32con.MB_ICONWARNING)

    def download(self, pro):
        musicpath = cfg.get(cfg.downloadFolder)
        if pro == "200":
            self.pro_bar.setValue(100)
            u = open("log\\list_download.json", "r")
            data = json.loads(u.read())
            u.close()
            song = data["song"]
            singer = data["singer"]
            album = data["album"]
            path = "{}\\{} - {}.mp3".format(musicpath, singer, song)
            path = os.path.abspath(path)
            audio = EasyID3(path)
            audio['title'] = song
            audio['album'] = album
            audio["artist"] = singer
            audio.save()
            text = '音乐下载完成！\n歌曲名：{}\n艺术家：{}\n保存路径：{}'.format(song, singer, path)
            win32api.MessageBox(0, text, '音乐下载完成', win32con.MB_OK)
            self.TableWidget_2.clearSelection()
            self.PushButton_2.setEnabled(False)
            self.pro_bar.setHidden(True)
        else:
            self.pro_bar.setValue(int(pro))
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.SubtitleLabel.setText(_translate("self", "导入歌单"))
        self.SubtitleLabel_2.setText(_translate("self", "导入方式："))
        self.ComboBox.addItems(["用户", "歌单"])
        self.SubtitleLabel_3.setText(_translate("self", "ID/UID："))
        self.PushButton.setText(_translate("self", "导入"))
        self.PushButton_2.setText(_translate("self", "下载"))
        self.PushButton_2.setEnabled(False)


from qfluentwidgets import ComboBox, LineEdit, PushButton, SubtitleLabel, TableWidget, ProgressBar


def get_folders(folder_path):
    folders = []

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            folders.append(item)

    return folders


if __name__ == "__main__":
    import sys

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = playlist()
    ui.__init__()
    Form.show()
    sys.exit(app.exec_())
