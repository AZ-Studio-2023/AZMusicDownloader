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

        content = '''1.修改了音乐获取、下载的接口
2.下线了显示预览词，仅提供热歌预览词
3.修复了音乐库功能
4.添加了歌单功能（需打开beta实验功能）
5.歌单支持从其他音乐软件导入（50首以下）
6.修复了任务多线程
7.添加了启动界面，使软件启动过程不再单调
鸣谢 & Thanks：
ConiMite  辰墨 
        '''
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='AZ音乐下载器v2.0.0更新日志',
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