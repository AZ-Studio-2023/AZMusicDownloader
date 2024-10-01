from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QHBoxLayout, QVBoxLayout, QHeaderView
from qfluentwidgets import ComboBox, LineEdit, PushButton, SubtitleLabel, TableWidget, ProgressBar, PrimaryPushButton, \
    MessageBoxBase
from qfluentwidgets import FluentIcon as FIF

from helper.downloadHelper import downloading, download
from helper.flyoutmsg import setOK
from helper.playlistHelper import getlist, FindLists, searchstart, music, search, rundownload


class playlist(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('playlist')
        self.resize(635, 700)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self)
        
        self.SubtitleLabel = SubtitleLabel("歌单", self)
        self.SubtitleLabel.setObjectName("SubtitleLabel")
        
        self.ChooseBox = PrimaryPushButton(FIF.ALBUM, "选择歌单", self)
        self.ChooseBox.clicked.connect(self.ChangePlaylist)
        self.StartBox = PushButton("从第三方平台导入", self)
        self.StartBox.clicked.connect(self.StartPutIn)
        self.StartDownload = PrimaryPushButton("下载", self)
        self.StartDownload.setDisabled(True)
        self.StartDownload.setObjectName("PushButton_2")
        self.StartDownload.clicked.connect(lambda: rundownload(PushButton_2=self.StartDownload, pro_bar=self.pro_bar, 
                                                              TableWidget_2=self.TableWidget_2, parent=self, dworker=self.dworker))
        
        self.pro_bar = ProgressBar(self)
        self.pro_bar.setHidden(True)
        self.pro_bar.setMaximum(100)
        
        self.hBoxLayout.addStretch(10)
        self.hBoxLayout.addWidget(self.SubtitleLabel, Qt.AlignLeft)
        self.hBoxLayout.addStretch(100)
        self.hBoxLayout.addWidget(self.pro_bar, Qt.AlignRight)
        self.hBoxLayout.addStretch(5)
        self.hBoxLayout.addWidget(self.ChooseBox, Qt.AlignRight)
        self.hBoxLayout.addStretch(5)
        self.hBoxLayout.addWidget(self.StartBox, Qt.AlignRight)
        self.hBoxLayout.addStretch(5)
        self.hBoxLayout.addWidget(self.StartDownload, Qt.AlignRight)
        self.hBoxLayout.addStretch(10)

        self.TableWidget_2 = TableWidget(self)
        self.TableWidget_2.setObjectName("TableWidget_2")
        self.TableWidget_2.setWordWrap(False)
        self.TableWidget_2.setColumnCount(4)
        self.TableWidget_2.verticalHeader().hide()
        self.TableWidget_2.setHorizontalHeaderLabels(['ID', '歌曲名', '艺术家', '专辑'])
        self.TableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TableWidget_2.itemSelectionChanged.connect(self.openbutton)
        self.TableWidget_2.resizeColumnsToContents()
        self.TableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.vBoxLayout.addLayout(self.hBoxLayout, Qt.AlignTop)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.TableWidget_2, Qt.AlignBottom)
        
        self.lworker = getlist()
        self.dworker = downloading(howto = "playlist")
        self.dworker.finished.connect(lambda Progress: download(progress = Progress, table = self.TableWidget_2, progressbar=self.pro_bar, 
                            songdata=None, dworker=self.dworker, button=self.StartDownload, parent=self.window(), howto = "lists"))

    def openbutton(self):
        self.StartDownload.setEnabled(True)
    def StartPutIn(self):
        w = PutIn(parent=self)
        if w.exec():
            setOK(parent=self, howto="playlists")
    def ChangePlaylist(self):
        w = ChoosePlayList(parent=self)
        w.exec()

class PutIn(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent.window())
        self.titleLabel = SubtitleLabel('导入歌单', self)
        self.api_type = QHBoxLayout(self)
        self.howtoin = QHBoxLayout(self)
        self.inUID = QHBoxLayout(self)
        self.Api_Tips = SubtitleLabel("API：", self)
        self.Api_Tips.setObjectName("Api_Tips")
        self.SubtitleLabel_2 = SubtitleLabel("导入方式：", self)
        self.SubtitleLabel_2.setObjectName("SubtitleLabel_2")
        self.SubtitleLabel_3 = SubtitleLabel("ID/UID：", self)
        self.SubtitleLabel_3.setObjectName("SubtitleLabel_3")

        self.apiBox = ComboBox(self)
        self.apiBox.addItems(["NCMA"])
        self.ComboBox = ComboBox(self)
        self.ComboBox.setObjectName("ComboBox")
        self.ComboBox.addItems(["用户", "歌单"])
        self.LineEdit = LineEdit(self)
        self.LineEdit.setObjectName("LineEdit")
        
        # add widget to view layout
        self.api_type.addWidget(self.Api_Tips)
        self.api_type.addWidget(self.apiBox)
        self.howtoin.addWidget(self.SubtitleLabel_2)
        self.howtoin.addWidget(self.ComboBox)
        self.inUID.addWidget(self.SubtitleLabel_3)
        self.inUID.addWidget(self.LineEdit)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(self.api_type)
        self.viewLayout.addLayout(self.howtoin)
        self.viewLayout.addLayout(self.inUID)
        
        # change the text of button
        self.yesButton.setText('导入')
        self.yesButton.setDisabled(True)
        self.cancelButton.setText('取消')
        self.yesButton.clicked.connect(lambda: searchstart(PushButton=self.yesButton, lworker=parent.lworker,
                                                            ComboBox=self.ComboBox, LineEdit=self.LineEdit, parent=parent))
        self.widget.setMinimumWidth(350)
        self.LineEdit.textChanged.connect(self._validateText)

        # self.hideYesButton()

    def _validateText(self, text):
        if text == None:
            self.yesButton.setDisabled(True)
        else:
            self.yesButton.setEnabled(True)

class ChoosePlayList(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent.window())
        self.titleLabel = SubtitleLabel('选择歌单', self)
        
        self.TableWidget = TableWidget(self)
        self.TableWidget.setObjectName("TableWidget")
        self.TableWidget.setWordWrap(False)
        self.TableWidget.setRowCount(30)
        self.TableWidget.setColumnCount(2)
        self.TableWidget.verticalHeader().hide()
        self.TableWidget.setHorizontalHeaderLabels(['序号', '歌单'])
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.TableWidget.resizeColumnsToContents()
        self.TableWidget.resizeColumnsToContents()
        self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.TableWidget.itemSelectionChanged.connect(lambda: self.yesButton.setEnabled(True))
        FindLists(TableWidget=self.TableWidget)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.TableWidget)

        # change the text of button
        self.yesButton.setText('确定')
        self.yesButton.setDisabled(True)
        self.cancelButton.setText('取消')
        self.yesButton.clicked.connect(lambda: music(TableWidget=self.TableWidget, TableWidget_2=parent.TableWidget_2, Button=parent.ChooseBox, parent=parent))
        parent.lworker.finished.connect(lambda: search(lworker=parent.lworker, TableWidget=self.TableWidget))

        self.widget.setMinimumWidth(350)