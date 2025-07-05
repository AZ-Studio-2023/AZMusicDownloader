# coding: utf-8
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QStyleOptionViewItem, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QHeaderView, \
    QAbstractItemView
from qfluentwidgets import TableWidget, isDarkTheme, TableItemDelegate, SearchLineEdit, \
    PrimaryPushButton, SpinBox, ProgressBar, BodyLabel, IndeterminateProgressBar
from PyQt5.QtCore import QObject
import helper.config
from helper.inital import get_update, showup
from helper.downloadHelper import downloading, download
from helper.searchmusicHelper import getlist, sethotlineEdit, search, searchstart, rundownload
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

        self.SearchLabel = BodyLabel('输入歌曲名/歌手/专辑名', self)
        self.lineEdit = SearchLineEdit(self)
        self.lineEdit.setPlaceholderText('搜索音乐')
        self.lineEdit.setFixedSize(200, 33)

        # self.lineEdit.textEdited.connect(self.keys)
        StartSearch =  lambda: searchstart(lineEdit=self.lineEdit, parent=self, spinBox=self.spinBox, lworker=self.lworker, progressbar=self.IndeterminateProgressBar)
        self.lineEdit.returnPressed.connect(StartSearch)
        self.lineEdit.searchButton.released.connect(StartSearch)

        self.numLabel = BodyLabel('显示数量', self)
        self.spinBox = SpinBox(self)
        self.spinBox.setValue(15)

        # self.worker_thread = QThread()
        # self.worker = Worker()
        # self.worker.moveToThread(self.worker_thread)

        self.lworker = getlist()
        self.dworker = downloading(howto="search")
        self.upworker = get_update()
        self.lworker.finished.connect(lambda: search(progressbar=self.IndeterminateProgressBar, lworker=self.lworker, parent=self,
                                                     tableView=self.tableView, spinBox=self.spinBox))
        self.dworker.finished.connect(
            lambda Progress: download(progress=Progress, table=self.tableView, progressbar=self.ProgressBar,
                                      songdata=self.lworker.songInfos, dworker=self.dworker, button=self.primaryButton1,
                                      parent=self.window(), howto="search"))
        self.upworker.finished.connect(
            lambda updata: showup(parent=self.window(), updata=updata, upworker=self.upworker))
        # self.worker.finished.connect(self.on_worker_finished)

        self.primaryButton1 = PrimaryPushButton('下载', self)
        self.primaryButton1.released.connect(lambda: rundownload(parent=self, primaryButton1=self.primaryButton1,
                                                                 tableView=self.tableView, dworker=self.dworker,
                                                                 lworker=self.lworker, ProgressBar=self.ProgressBar))
        self.primaryButton1.setEnabled(False)

        self.ProgressBar = ProgressBar(self)
        self.ProgressBar.setHidden(True)
        self.ProgressBar.setMaximum(100)
        self.ProgressBar.setFixedWidth(200)

        self.IndeterminateProgressBar = IndeterminateProgressBar(self, start=True)
        self.IndeterminateProgressBar.setHidden(True)
        self.IndeterminateProgressBar.setMaximum(100)
        self.IndeterminateProgressBar.setFixedWidth(200)

        self.layout1.addStretch(100)
        self.layout1.addWidget(self.SearchLabel)
        self.layout1.addSpacing(10)
        self.layout1.addWidget(self.lineEdit)
        self.layout1.addSpacing(10)
        self.layout1.addWidget(self.numLabel)
        self.layout1.addSpacing(10)
        self.layout1.addWidget(self.spinBox)
        self.layout1.addSpacing(10)
        self.layout1.addWidget(self.primaryButton1)
        self.layout1.addSpacing(10)
        self.layout1.addWidget(self.ProgressBar)
        self.layout1.addWidget(self.IndeterminateProgressBar)
        self.layout1.addStretch(100)

        self.tableView = TableWidget(self)

        # self.tableView.setItemDelegate(CustomTableItemDelegate(self.tableView))

        self.tableView.setWordWrap(False)
        self.tableView.setColumnCount(4)
        # songInfos = []
        # songInfos += songInfos
        # for i, songInfo in enumerate(songInfos):
        #     for j in range(4):
        #         self.tableView.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.tableView.verticalHeader().hide()
        if helper.config.pfg.apicard.value == "Bilibili":
            self.tableView.setHorizontalHeaderLabels(['BV号', '歌曲名', 'UP主', '原标题'])
        else:
            self.tableView.setHorizontalHeaderLabels(['ID', '歌曲名', '艺术家', '专辑'])
        self.tableView.resizeColumnsToContents()
        self.tableView.itemSelectionChanged.connect(self.openbutton)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableView.setSortingEnabled(True)
        # self.tableView.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(30, 20, 60, 20)
        self.hBoxLayout.addWidget(self.tableView)
        self.hBoxLayout.addSpacing(60)
        self.hBoxLayout.addLayout(self.layout1)

        self.resize(635, 700)

        sethotlineEdit(lineEdit=self.lineEdit)
        if helper.config.Config.update_card.value == False:
            self.upworker.start()

    def openbutton(self):
        self.primaryButton1.setEnabled(True)

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
