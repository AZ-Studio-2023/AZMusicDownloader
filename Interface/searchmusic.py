# coding: utf-8
import json, random, AZMusicAPI, webbrowser
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QStyleOptionViewItem, QTableWidgetItem, QWidget, QHBoxLayout, \
    QVBoxLayout, QLabel, QCompleter, QHeaderView
from qfluentwidgets import TableWidget, isDarkTheme, TableItemDelegate, SearchLineEdit, \
    PrimaryPushButton, SpinBox, InfoBar, InfoBarPosition, InfoBarIcon, PushButton, ProgressBar
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import helper.config
import requests, os
from json import loads
from mutagen.easyid3 import EasyID3
from helper.config import cfg
from helper.getvalue import apipath, download_log, search_log, autoapi, adurl
from helper.inital import mkf
from helper.flyoutmsg import dlsuc, dlerr, dlwar

try:
    u = open(apipath, "r")
    data = json.loads(u.read())
    api = data["api"]
    u.close()   
except:
    api = autoapi
mkf()

def is_english_and_characters(input_string):
    return all(char.isalpha() or not char.isspace() for char in input_string)

class getlist(QThread):
    finished = pyqtSignal()

    @pyqtSlot()
    def run(self):
        u = open(search_log, "r")
        data = json.loads(u.read())
        u.close()
        text = data["text"]
        value = data["value"]
        api_value = data["api_value"]
        keywords = text
        self.songInfos = AZMusicAPI.getmusic(keywords, number=value, api=api_value)
        self.finished.emit()


class downloading(QThread):
    finished = pyqtSignal(str)

    @pyqtSlot()
    def run(self):
        musicpath = cfg.get(cfg.downloadFolder)
        u = open(download_log, "r")
        data = json.loads(u.read())
        u.close()
        id = data["id"]
        api = data["api"]
        song = data["song"]
        singer = data["singer"]
        url = AZMusicAPI.geturl(id=id, api=api)
        if url == "Error 3":
            dlerr(content='这首歌曲无版权，暂不支持下载', parent=self)
            return 0
        elif url == "NetworkError":
            dlerr(content='您可能是遇到了以下其一问题：网络错误 / 服务器宕机 / IP被封禁', parent = self)
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


# class Worker(QObject):
#     finished = pyqtSignal()
#
#     @pyqtSlot()
#     def do_work(self, text):
#         if helper.config.Config.twitcard.value == True and is_english_and_characters(text):
#             try:
#                 self.key = AZMusicAPI.searchkey(text)mn
#             except:
#                 self.key = []
#                 return 0
#             if "Error" in self.key:
#                 self.key = []
#                 return 0
#         else:
#             self.key = []
#
#         self.finished.emit()


class CustomTableItemDelegate(TableItemDelegate):
    """ Custom table item delegate """

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        super().initStyleOption(option, index)
        if index.column() != 1:
            return

        if isDarkTheme():
            option.palette.setColor(QPalette.Text, Qt.white)
            option.palette.setColor(QPalette.HighlightedText, Qt.white)
        else:
            option.palette.setColor(QPalette.Text, Qt.red)
            option.palette.setColor(QPalette.HighlightedText, Qt.red)


def getad():
    url = adurl
    try:
        ad = requests.get(url).text
        data = loads(ad)
        msg = data
    except:
        try:
            o = open("resource/hitokoto.json", "r")
            hit_data = json.loads(o.read())["hitokoto"]
            o.close()
            poem = hit_data[random.randint(0, len(hit_data) - 1)]
        except:
            poem = "海内存知己，天涯若比邻"
        ad = {"title": "(⊙o⊙)？", "text": "呀！找不到广告了 ＞﹏＜ 请检查您的网络连接\n{}".format(poem), "time": 30000,
              "button": "（；´д｀）ゞ", "url": "https://azstudio.net.cn"}
        msg = ad
    return msg


class get_ad(QThread):
    finished = pyqtSignal(dict)

    @pyqtSlot()
    def run(self):
        data = getad()
        self.finished.emit(data)


class searchmusic(QWidget, QObject):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setObjectName("searchmusic")
        
        self.hBoxLayout = QHBoxLayout(self)
        self.layout1 = QVBoxLayout(self)

        self.empty1 = QLabel('', self)
        self.empty2 = QLabel('', self)
        self.empty3 = QLabel('', self)
        self.empty4 = QLabel('', self)
        self.empty5 = QLabel('', self)
        self.empty6 = QLabel('', self)
        self.empty7 = QLabel('', self)
        self.empty8 = QLabel('', self)
        self.empty9 = QLabel('', self)
        self.empty10 = QLabel('', self)
        self.empty11 = QLabel('', self)
        self.empty12 = QLabel('', self)
        self.empty13 = QLabel('', self)
        self.empty14 = QLabel('', self)
        self.empty15 = QLabel('', self)
        self.empty16 = QLabel('', self)
        self.empty17 = QLabel('', self)
        self.empty18 = QLabel('', self)
        self.empty19 = QLabel('', self)
        self.empty20 = QLabel('', self)
        self.empty21 = QLabel('', self)
        self.empty22 = QLabel('', self)
        self.empty23 = QLabel('', self)
        self.empty24 = QLabel('', self)

        self.layout1.addWidget(self.empty19)
        self.layout1.addWidget(self.empty20)
        self.layout1.addWidget(self.empty21)
        self.layout1.addWidget(self.empty22)
        self.layout1.addWidget(self.empty23)
        self.layout1.addWidget(self.empty24)

        self.lineEdit = SearchLineEdit(self)
        self.lineEdit.setFixedSize(200, 33)
        self.empty50 = QLabel('输入歌曲名/歌手/专辑名', self)
        self.lineEdit.setPlaceholderText('搜索音乐')
        # self.lineEdit.textEdited.connect(self.keys)
        self.lineEdit.returnPressed.connect(self.searchstart)
        self.lineEdit.searchButton.released.connect(self.searchstart)
        self.layout1.addWidget(self.empty50)
        self.layout1.addWidget(self.lineEdit)
        self.empty = QLabel('显示数量', self)
        self.spinBox = SpinBox(self)
        self.spinBox.setValue(15)
        # self.empty0 = QLabel('第几页', self)
        # self.spinBox0 = SpinBox(self)
        self.layout1.addWidget(self.empty)
        self.layout1.addWidget(self.spinBox)
        # self.layout1.addWidget(self.empty0)
        # self.layout1.addWidget(self.spinBox0)
        # self.worker_thread = QThread()
        # self.worker = Worker()
        # self.worker.moveToThread(self.worker_thread)

        self.lworker = getlist()

        self.dworker = downloading()

        self.adworker = get_ad()

        # self.worker.finished.connect(self.on_worker_finished)
        self.lworker.finished.connect(self.search)
        self.dworker.finished.connect(self.download)
        self.adworker.finished.connect(self.showad)
        self.primaryButton1 = PrimaryPushButton('下载', self)
        self.primaryButton1.released.connect(self.rundownload)
        self.primaryButton1.setEnabled(False)
        self.ProgressBar = ProgressBar(self)
        self.ProgressBar.setHidden(True)
        self.ProgressBar.setMaximum(100)
        self.ProgressBar.setFixedWidth(200)
        self.layout1.addWidget(self.ProgressBar)
        self.layout1.addWidget(self.primaryButton1)

        self.layout1.addWidget(self.empty13)
        self.layout1.addWidget(self.empty14)
        self.layout1.addWidget(self.empty15)
        self.layout1.addWidget(self.empty16)
        self.layout1.addWidget(self.empty17)
        self.layout1.addWidget(self.empty18)

        self.tableView = TableWidget(self)

        # self.tableView.setItemDelegate(CustomTableItemDelegate(self.tableView))

        self.tableView.setWordWrap(False)
        self.tableView.setRowCount(25)
        self.tableView.setColumnCount(4)
        # songInfos = []
        # songInfos += songInfos
        # for i, songInfo in enumerate(songInfos):
        #     for j in range(4):
        #         self.tableView.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(['ID', '歌曲名', '艺术家', '专辑'])
        self.tableView.resizeColumnsToContents()
        self.tableView.itemSelectionChanged.connect(self.openbutton)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.setSortingEnabled(True)
        # self.tableView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.tableView.selectionChanged(self.nm)

        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout.addWidget(self.tableView)
        self.hBoxLayout.addWidget(self.empty7)
        self.hBoxLayout.addWidget(self.empty8)
        self.hBoxLayout.addWidget(self.empty9)
        self.hBoxLayout.addWidget(self.empty10)
        self.hBoxLayout.addWidget(self.empty11)
        self.hBoxLayout.addWidget(self.empty12)
        self.hBoxLayout.addLayout(self.layout1)
        self.hBoxLayout.addWidget(self.empty1)
        self.hBoxLayout.addWidget(self.empty2)
        self.hBoxLayout.addWidget(self.empty3)
        self.hBoxLayout.addWidget(self.empty4)
        self.hBoxLayout.addWidget(self.empty5)
        self.hBoxLayout.addWidget(self.empty6)
        self.resize(635, 700)
        if helper.config.Config.adcard.value == False:
            self.adworker.start()
        if helper.config.cfg.hotcard.value:
            try:
                data = requests.get(api + "search/hot").json()["result"]["hots"]
                hot_song = []
                for i in data:
                    hot_song.append(i["first"])
                self.completer = QCompleter(hot_song, self.lineEdit)
                self.completer.setCaseSensitivity(Qt.CaseInsensitive)
                self.completer.setMaxVisibleItems(10)
                self.lineEdit.setCompleter(self.completer)
            except:
                pass

    def openlk(self):
        webbrowser.open_new_tab(self.ad["url"])

    def openbutton(self):
        self.primaryButton1.setEnabled(True)

    def showad(self, addata):
        self.ad = addata
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title=self.ad["title"],
            content=self.ad["text"],
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=self.ad["time"],
            parent=self
        )

        self.s = PushButton(self.ad["button"])
        w.addWidget(self.s)
        self.s.clicked.connect(self.openlk)
        w.show()
        self.adworker.quit()

    @pyqtSlot()
    def searchstart(self):
        # self.lworker.started.connect(
        #     lambda: self.lworker.run(text=self.lineEdit.text(), value=self.spinBox.value(), api_value=api))
        u = open(search_log, "w")
        u.write(json.dumps({"text": self.lineEdit.text(), "api_value": api, "value": self.spinBox.value()}))
        u.close()
        self.lworker.start()

    # @pyqtSlot()
    # def keys(self):
    #     self.worker_thread.started.connect(lambda: self.worker.do_work(text=self.lineEdit.text()))
    #     self.worker_thread.start()

    @pyqtSlot()
    def rundownload(self):
        musicpath = cfg.get(cfg.downloadFolder)
        self.primaryButton1.setEnabled(False)
        self.ProgressBar.setHidden(False)
        self.ProgressBar.setValue(0)
        row = self.tableView.currentIndex().row()
        try:
            data = self.songdata[row]
        except:
            dlerr(content='您选中的行无数据', parent=self)
            return 0
        song_id = data["id"]
        song = data["name"]
        singer = data["artists"]
        try:
            if os.path.exists(musicpath) == False:
                os.mkdir(musicpath)
        except:
            dlerr(content='音乐下载路径无法读取\创建失败', parent=self)
            return 0
        # self.dworker.started.connect(lambda: self.dworker.run(id=song_id, api=api, song=song, singer=singer))
        u = open(download_log, 'w')
        u.write(json.dumps({"id": song_id, "api": api, "song": song, "singer": singer}))
        u.close()
        self.dworker.start()

    # @pyqtSlot()
    # def on_worker_finished(self):
    #     self.completer = QCompleter(self.worker.key, self.lineEdit)
    #     self.completer.setCaseSensitivity(Qt.CaseInsensitive)
    #     self.lineEdit.setCompleter(self.completer)
    #     self.worker_thread.quit()

    @pyqtSlot()
    def search(self):
        songInfos = self.lworker.songInfos
        if songInfos == "Error 0":
            dlwar(content='未搜索到相关的歌曲，换个关键词试试吧', parent=self)
            return 0
        elif songInfos == "Error 1":
            dlwar(content='你还没有输入噢', parent=self)
            return 0
        elif songInfos == "NetworkError":
            dlerr(content='您可能是遇到了以下其一问题：网络错误 / 服务器宕机 / IP被封禁', parent = self)
            return 0
        self.songdata = songInfos
        self.tableView.setRowCount(self.spinBox.value())
        for i in range(len(songInfos)):
            data = songInfos[i]
            num = i + 1
            song_id = data["id"]
            title = data["name"]
            Artist = data["artists"]
            Album = data["album"]

            if len(title) > 8:
                title = title[:8] + "..."
            if len(Artist) > 8:
                Artist = Artist[:8] + "..."
            if len(Album) > 8:
                Album = Album[:8] + "..."
            data = []
            data.append(str(song_id))
            data.append(title)
            data.append(Artist)
            data.append(Album)
            for j in range(4):
                self.tableView.setItem(i, j, QTableWidgetItem(data[j]))
        self.tableView.resizeColumnsToContents()
        self.lworker.quit()

    def download(self, progress):
        musicpath = cfg.get(cfg.downloadFolder)
        if progress == "200":
            self.ProgressBar.setValue(100)
            row = self.tableView.currentIndex().row()
            try:
                data = self.songdata[row]
            except:
                dlerr(content='您选中的行无数据', parent=self)
            song_id = data["id"]
            song = data["name"]
            singer = data["artists"]
            album = data["album"]
            self.dworker.quit()
            self.tableView.clearSelection()
            self.primaryButton1.setEnabled(False)
            path = "{}\\{} - {}.mp3".format(musicpath, singer, song)
            path = os.path.abspath(path)
            audio = EasyID3(path)
            audio['title'] = song
            audio['album'] = album
            audio["artist"] = singer
            audio.save()
            text = '音乐下载完成！\n歌曲名：{}\n艺术家：{}\n保存路径：{}'.format(song, singer, path)
            dlsuc(content=text, parent=self)
            self.ProgressBar.setHidden(True)
        else:
            self.ProgressBar.setValue(int(progress))
