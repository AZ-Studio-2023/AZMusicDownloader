import sys

from PyQt5.QtCore import Qt, QSize, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QAction, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (Action, DropDownPushButton, DropDownToolButton, PushButton, PrimaryPushButton,
                            HyperlinkButton, setTheme, Theme, ToolButton, ToggleButton, RoundMenu,
                            SplitPushButton, SplitToolButton, PrimaryToolButton, PrimarySplitPushButton,
                            PrimarySplitToolButton, PrimaryDropDownPushButton, PrimaryDropDownToolButton,
                            TogglePushButton, ToggleToolButton, TransparentPushButton, TransparentToolButton,
                            TransparentToggleToolButton, TransparentTogglePushButton, TransparentDropDownToolButton,InfoBarIcon, InfoBar, InfoBarPosition, InfoBarManager, 
                            TransparentDropDownPushButton, PillPushButton, PillToolButton, TitleLabel)
from qfluentwidgets import FluentIcon as FIF

class player(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('player')
        # setTheme(Theme.DARK)
        self.setStyleSheet('start{background:white}')

        content = "我们正在努力开发这个功能，但这需要一段时间，请理解我们。您可以先使用AZ Studio的其它播放器。如果可以，欢迎赞助我们或加入我们一起开发，甚至是提点建议都是对我们的帮助啦(●'◡'●)"
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='很抱歉，这个功能还没有上线',
            content=content,
            orient=Qt.Vertical,    # vertical layout
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=-1,
            parent=self
        )
        w.addWidget(PushButton('赞助我们'))
        w.addWidget(PushButton('加入我们'))
        w.addWidget(PushButton('提交反馈'))
        w.show()

        self.resize(800, 800)

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w2 = start()
    w2.show()
    app.exec_()