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

class note(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('note')
        # setTheme(Theme.DARK)
        self.setStyleSheet('start{background:white}')

        content = '''1.修复了系统音乐文件夹修改后无法下载的问题
鸣谢 & Thanks：
ConiMite  辰墨 
        '''
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='AZMusicDownloader v2.1.0 Update 2更新日志',
            content=content,
            orient=Qt.Vertical,    # vertical layout
            isClosable=False,
            position=InfoBarPosition.TOP,
            duration=-1,
            parent=self
        )
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