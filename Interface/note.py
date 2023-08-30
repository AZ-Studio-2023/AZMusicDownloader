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

        content = '''
        哈喽哈喽，欢迎使用AZ Studio打造的AZ音乐下载器。下面来看看初版有哪些功能吧：
        1.免费下载高品质音乐：免费下载音乐（除单曲付费外）
        2.多元性的设置
        3.搜索提示
        4.自定义搜索数量
        5.我们单独把搜索音乐、获得音乐地址的功能拎出来做了一个库：AZMusicAPI 欢迎大家使用！
        '''
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='AZ音乐下载器V1.0更新日志',
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