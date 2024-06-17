from PyQt5.QtWidgets import QWidget, QAbstractItemView
from qfluentwidgets import ComboBox, LineEdit, PushButton, SubtitleLabel, TableWidget, ProgressBar
from PyQt5 import QtCore
from helper.downloadHelper import downloading, download
from helper.playlistHelper import getlist, FindLists, searchstart, music, search, rundownload



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
        self.PushButton.clicked.connect(lambda: searchstart(PushButton=self.PushButton, lworker=self.lworker,
                                                            ComboBox=self.ComboBox, LineEdit=self.LineEdit, parent=self))
        
        self.TableWidget = TableWidget(self)
        self.TableWidget.setGeometry(QtCore.QRect(15, 11, 281, 601))
        self.TableWidget.setObjectName("TableWidget")
        self.TableWidget.setWordWrap(False)
        self.TableWidget.setRowCount(30)
        self.TableWidget.setColumnCount(2)
        self.TableWidget.verticalHeader().hide()
        self.TableWidget.setHorizontalHeaderLabels(['序号', '歌单'])
        self.TableWidget.cellDoubleClicked.connect(lambda: music(TableWidget=self.TableWidget, TableWidget_2=self.TableWidget_2, parent=self))
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
        self.PushButton_2.clicked.connect(lambda: rundownload(PushButton_2=self.PushButton_2, pro_bar=self.pro_bar, 
                                                              TableWidget_2=self.TableWidget_2, parent=self, dworker=self.dworker))
        
        self.pro_bar = ProgressBar(self)
        self.pro_bar.setGeometry(QtCore.QRect(380, 410, 102, 32))
        self.pro_bar.setHidden(True)
        self.pro_bar.setMaximum(100)
        
        self.lworker = getlist()
        self.lworker.finished.connect(lambda: search(PushButton=self.PushButton, lworker=self.lworker, TableWidget=self.TableWidget))
        self.dworker = downloading(howto = "playlist")
        self.dworker.finished.connect(lambda Progress: download(progress = Progress, table = self.TableWidget_2, progressbar=self.pro_bar, 
                            songdata=None, dworker=self.dworker, button=self.PushButton_2, parent=self, howto = "lists"))
        
        self.retranslateUi()
        FindLists(TableWidget=self.TableWidget)
        self.TableWidget.resizeColumnsToContents()
        QtCore.QMetaObject.connectSlotsByName(self)

    def openbutton(self):
        self.PushButton_2.setEnabled(True)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.SubtitleLabel.setText(_translate("self", "导入歌单"))
        self.SubtitleLabel_2.setText(_translate("self", "导入方式："))
        self.ComboBox.addItems(["用户", "歌单"])
        self.SubtitleLabel_3.setText(_translate("self", "ID/UID："))
        self.PushButton.setText(_translate("self", "导入"))
        self.PushButton_2.setText(_translate("self", "下载"))
        self.PushButton_2.setEnabled(False)

