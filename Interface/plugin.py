import json
import os
import sys

from PyQt5.QtCore import Qt, QPoint, QSize, QUrl, QRect
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy

from qfluentwidgets import (CardWidget, setTheme, Theme, IconWidget, BodyLabel, CaptionLabel, PushButton,
                            TransparentToolButton, FluentIcon, RoundMenu, Action, ElevatedCardWidget,
                            ImageLabel, isDarkTheme, FlowLayout, MSFluentTitleBar, SimpleCardWidget,
                            HeaderCardWidget, InfoBarIcon, HyperlinkLabel, HorizontalFlipView,
                            PrimaryPushButton, TitleLabel, PillPushButton, setFont, SingleDirectionScrollArea,
                            VerticalSeparator)

from qfluentwidgets.components.widgets.acrylic_label import AcrylicBrush



def get_folders(directory):
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folders.append(item)
    return folders

class Plugins_Card(CardWidget):

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        # self.openButton = PushButton('详情', self)
        # self.moreButton = TransparentToolButton(FluentIcon.MORE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        # self.openButton.setFixedWidth(120)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        # self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignRight)
        # self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignRight)
        # self.moreButton.setFixedSize(32, 32)


class plugins(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setObjectName("plugins")

        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(30, 60, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        for folder in get_folders("plugins"):
            get_json = open(f"plugins/{folder}/index.json", "r", encoding="utf-8")
            data = json.loads(get_json.read())
            get_json.close()
            self.addCard(data["icon"], data["name"], data["desc"])



    def addCard(self, icon, title, content):
        card = Plugins_Card(icon, title, content, self)
        self.vBoxLayout.addWidget(card, alignment=Qt.AlignTop)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = plugins()
    w.show()
    app.exec_()
