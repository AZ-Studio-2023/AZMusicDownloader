# coding: utf-8
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QHeaderView, QAbstractItemView
from qfluentwidgets import TableWidget
from helper.config import cfg
from helper.localmusicsHelper import ref, openthemusic


class localmusics(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("localmusics")
        self.hBoxLayout = QHBoxLayout(self)
        self.local_view = TableWidget(self)
        self.local_view.setColumnCount(4)
        self.local_view.verticalHeader().hide()
        self.local_view.setHorizontalHeaderLabels(['路径', '歌曲名', '艺术家', '专辑'])
        self.local_view.resizeColumnsToContents()
        self.local_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.local_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        ref(local_view=self.local_view, musicpath=cfg.get(cfg.downloadFolder))

        self.hBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.local_view.cellDoubleClicked.connect(lambda: openthemusic(filepath=cfg.get(cfg.downloadFolder)))
        self.resize(635, 700)
        self.hBoxLayout.addWidget(self.local_view)