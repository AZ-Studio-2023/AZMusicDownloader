import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class player(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('player')
        layout = QVBoxLayout()
        self.setWindowTitle('Music Player')
        self.setGeometry(5, 30, 1355, 730)
        self.browser = QWebEngineView()
        self.browser.load(QUrl('https://json.zenglingkun.cn/player.html'))
        layout.addWidget(self.browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = player()
    win.show()
    app.exit(app.exec_())
