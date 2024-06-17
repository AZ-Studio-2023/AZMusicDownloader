# coding: utf-8
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QStyleOptionViewItem, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QHeaderView
from qfluentwidgets import TableWidget, isDarkTheme, TableItemDelegate, SearchLineEdit, \
    PrimaryPushButton, SpinBox, ProgressBar
from PyQt5.QtCore import QObject
import helper.config
from helper.inital import get_update, showup
from helper.downloadHelper import downloading, download
from helper.searchmusicHelper import getlist, sethotlineEdit, search, searchstart, rundownload

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
        self.lineEdit.returnPressed.connect(lambda: searchstart(lineEdit=self.lineEdit, parent=self, spinBox=self.spinBox, lworker=self.lworker))
        self.lineEdit.searchButton.released.connect(lambda: searchstart(lineEdit=self.lineEdit, parent=self, spinBox=self.spinBox, lworker=self.lworker))
        
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
        self.dworker = downloading(howto="search")       
        self.upworker = get_update()
        self.lworker.finished.connect(lambda: search(lworker=self.lworker, parent=self,
                        tableView=self.tableView, spinBox=self.spinBox))
        self.dworker.finished.connect(lambda Progress: download(progress = Progress, table = self.tableView, progressbar=self.ProgressBar, 
                            songdata=self.lworker.songInfos, dworker=self.dworker, button=self.primaryButton1, parent=self, howto = "search"))
        self.upworker.finished.connect(self.showupupgrade)
        # self.worker.finished.connect(self.on_worker_finished)

        self.primaryButton1 = PrimaryPushButton('下载', self)
        self.primaryButton1.released.connect(lambda: rundownload(parent=self, primaryButton1=self.primaryButton1,
                            tableView=self.tableView, dworker=self.dworker, lworker=self.lworker, ProgressBar=self.ProgressBar))
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
        
        sethotlineEdit(lineEdit=self.lineEdit)
        if helper.config.Config.update_card.value == False:
            self.upworker.start()
        
    def openbutton(self):
        self.primaryButton1.setEnabled(True)

    def showupupgrade(self, updata):
        showup(parent = self, updata = updata, upworker = self.upworker)

    # @pyqtSlot()
    # def keys(self):
    #     self.worker_thread.started.connect(lambda: self.worker.do_work(text=self.lineEdit.text()))
    #     self.worker_thread.start()

    # @pyqtSlot()
    # def on_worker_finished(self):
    #     self.completer = QCompleter(self.worker.key, self.lineEdit)
    #     self.completer.setCaseSensitivity(Qt.CaseInsensitive)
    #     self.lineEdit.setCompleter(self.completer)
    #     self.worker_thread.quit()