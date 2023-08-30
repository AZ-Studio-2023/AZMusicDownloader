# coding: utf-8
import sys
import AZMusicAPI
import webbrowser
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtCore import QTimer,QThread
from PyQt5.QtGui import QPalette, QMouseEvent
from PyQt5.QtWidgets import QApplication, QStyleOptionViewItem, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QVBoxLayout, QLabel,QCompleter
import threading
from qfluentwidgets import TableWidget, isDarkTheme, setTheme, Theme, TableView, TableItemDelegate, SearchLineEdit, PrimaryPushButton, SpinBox, InfoBar, InfoBarPosition, InfoBarManager, InfoBarIcon,PushButton
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import helper.config
import win32api,win32con
import os
import requests
from json import loads

def is_english_and_characters(input_string):
    return all(char.isalpha() or not char.isspace() for char in input_string)

class getlist(QObject):
    finished = pyqtSignal()
    @pyqtSlot()
    def run(self,text,value):
        keywords = text
        self.songInfos = AZMusicAPI.getmusic(keywords,value)
        self.finished.emit()
        
class downloading(QObject):
    finished = pyqtSignal()
    @pyqtSlot()
    def run(self,rid,reqId,song,singer):
        url = AZMusicAPI.geturl(rid,reqId)
        musicpath = os.path.join(os.path.expanduser('~'), 'Music')
        if url == "Error 3":
            win32api.MessageBox(0,'这首歌曲需要单曲付费噢，暂不支持下载','错误',win32con.MB_ICONWARNING)
            return 0
        elif url == "NetError":
            win32api.MessageBox(0,'您可能是遇到了以下其一问题：网络错误 / 服务器宕机 / IP被封禁','错误',win32con.MB_ICONWARNING)
            return 0
        response = requests.get(url)
        response.raise_for_status()
        path = "{}\\AZMusicDownload\\{} - {}.mp3".format(musicpath,singer,song)
        path = os.path.abspath(path)
        if os.path.exists(path):
            return 0
        with open(path, 'wb') as file:
            file.write(response.content)
        text = '音乐下载完成！\n歌曲名：{}\n艺术家：{}\n保存路径：{}'.format(song,singer,path)
        win32api.MessageBox(0,text,'音乐下载完成',win32con.MB_OK)
        self.finished.emit()

class Worker(QObject):
    finished = pyqtSignal()
    @pyqtSlot()
    def do_work(self,text):
        if helper.config.Config.twitcard.value == True and is_english_and_characters(text) :
            try:
                self.key=AZMusicAPI.searchkey(text)
            except:
                self.key=[]
                return 0
            if "Error" in self.key:
                self.key=[]
                return 0
        else:
            self.key=[]

        self.finished.emit()
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



def getad(datas):
    url = "https://frp.azstudio.top/ad/music/home.json"
    try:
        ad = requests.get(url).text
        data = loads(ad)
        msg = data[datas]
    except:
        ad = {"title":"(⊙o⊙)？","text":"呀！找不到广告了 ＞﹏＜ 请检查您的网络连接","time":30000,"button":"（；´д｀）ゞ","url":"https://azstudio.top"}
        msg = ad[datas]
    return msg

class searchmusic(QWidget,QObject):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

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
        self.lineEdit.textEdited.connect(self.keys)
        self.lineEdit.returnPressed.connect(self.searchstart)
        self.lineEdit.searchButton.released.connect(self.searchstart)
        self.layout1.addWidget(self.empty50)
        self.layout1.addWidget(self.lineEdit)
        self.empty = QLabel('显示数量', self)
        self.spinBox = SpinBox(self)
        self.spinBox.setValue(15)
        #self.empty0 = QLabel('第几页', self)
        #self.spinBox0 = SpinBox(self)
        self.layout1.addWidget(self.empty)
        self.layout1.addWidget(self.spinBox)
        #self.layout1.addWidget(self.empty0)
        #self.layout1.addWidget(self.spinBox0)
        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)

        self.getlist_worker = QThread()
        self.lworker = getlist()
        self.lworker.moveToThread(self.getlist_worker) 

        self.download_worker = QThread()
        self.dworker = downloading()
        self.dworker.moveToThread(self.download_worker) 



        self.worker.finished.connect(self.on_worker_finished)   
        self.lworker.finished.connect(self.search) 
        self.dworker.finished.connect(self.download)    
        self.primaryButton1 = PrimaryPushButton('下载', self)
        self.primaryButton1.released.connect(self.rundownload)
        self.primaryButton1.setEnabled(False)
        self.layout1.addWidget(self.primaryButton1)
        
        self.layout1.addWidget(self.empty13)
        self.layout1.addWidget(self.empty14)
        self.layout1.addWidget(self.empty15)
        self.layout1.addWidget(self.empty16)
        self.layout1.addWidget(self.empty17)
        self.layout1.addWidget(self.empty18)

        self.tableView = TableWidget(self)

        # NOTE: use custom item delegate
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
        self.tableView.setHorizontalHeaderLabels(['序号','歌曲', '艺术家', '专辑'])
        self.tableView.resizeColumnsToContents()
        self.tableView.itemSelectionChanged.connect(self.openbutton)
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.setSortingEnabled(True)
        #self.tableView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        #self.tableView.selectionChanged(self.nm)

        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0,0)
        
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
            w = InfoBar(
                icon=InfoBarIcon.INFORMATION,
                title=getad("title"),
                content=getad("text"),
                orient=Qt.Vertical,    # vertical layout
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=getad("time"),
                parent=self
            )

            self.s = PushButton(getad("button"))
            w.addWidget(self.s)
            self.s.clicked.connect(self.openlk)
            w.show()
    def openlk(self):
        webbrowser.open_new_tab(getad("url"))
    def openbutton(self):
        self.primaryButton1.setEnabled(True)
    @pyqtSlot()
    def searchstart(self):
        self.getlist_worker.started.connect(lambda:self.lworker.run(text=self.lineEdit.text(),value=self.spinBox.value()))    
        self.getlist_worker.start()
    @pyqtSlot()
    def keys(self):
        self.worker_thread.started.connect(lambda:self.worker.do_work(text=self.lineEdit.text()))
        self.worker_thread.start()
    @pyqtSlot()
    def rundownload(self):
        self.primaryButton1.setEnabled(False)
        row = self.tableView.currentIndex().row() 
        data = self.songdata[row]
        rid = data["rid"]
        reqId = data["reqId"]
        song = data["songname"]
        singer = data["singer"]
        musicpath = os.path.join(os.path.expanduser('~'), 'Music')
        if os.path.exists(musicpath+"\\AZMusicDownload") == False:
            os.mkdir(musicpath+"\\AZMusicDownload")
        self.worker_thread.started.connect(lambda:self.dworker.run(rid=rid,reqId=reqId,song=song,singer=singer))
        self.worker_thread.start()        
    @pyqtSlot()
    def on_worker_finished(self):
        self.completer = QCompleter(self.worker.key, self.lineEdit)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(self.completer)
        self.worker_thread.quit()
    @pyqtSlot()
    def search(self):
        songInfos = self.lworker.songInfos
        if songInfos == "Error 0":
            win32api.MessageBox(0,'未搜索到相关的歌曲，换个关键词试试吧','错误',win32con.MB_ICONWARNING)
            return 0
        elif songInfos == "Error 1":
            win32api.MessageBox(0,'你还没有输入噢','错误',win32con.MB_ICONWARNING)
            return 0
        elif songInfos == "NetError":
            win32api.MessageBox(0,'您可能是遇到了以下其一问题：网络错误 / 服务器宕机 / IP被封禁','错误',win32con.MB_ICONWARNING)
            return 0
        self.songdata=songInfos
        self.tableView.setRowCount(self.spinBox.value())
        for i in range(len(songInfos)):
            data = songInfos[i]
            num = i+1
            title = data["songname"]
            Artist = data["singer"]
            Album = data["album"]
            if len(title) > 8:
                title=title[:8]+"..."
            if len(Artist) > 8:
                Artist=Artist[:8]+"..."
            if len(Album) > 8:
                Album=Album[:8]+"..."
            data=[]
            data.append(str(num))
            data.append(title)
            data.append(Artist)
            data.append(Album)
            for j in range(4):
                self.tableView.setItem(i, j, QTableWidgetItem(data[j]))
        self.tableView.resizeColumnsToContents()
        self.getlist_worker.quit()
    @pyqtSlot()
    def download(self):    
        self.download_worker.quit()
        self.tableView.clearSelection()
        self.primaryButton1.setEnabled(False)
        

        
if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = searchmusic()
    w.show()
    app.exec()
