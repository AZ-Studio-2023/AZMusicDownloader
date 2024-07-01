from sys import exit

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition, InfoBarIcon
from qfluentwidgets import PushButton, PrimaryPushButton, FlyoutView, Flyout

from helper.getvalue import outputlist, verdetail, VERSION, RELEASE_URL, AZ_URL


def getoutputvalue(outid):
    try:
        out=outputlist[int(outid)]
    except:
        out=outid
    return out

def changelog(parent):
    view = FlyoutView(
        title=f'AZMusicDownloader {VERSION}更新日志 ',
        content=verdetail,
        #image='resource/splash.png',
        isClosable=True
    )
        
    # add button to view
    button1 = PushButton(FIF.GITHUB, 'GitHub')
    button1.setFixedWidth(120)
    button1.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(RELEASE_URL)))
    view.addWidget(button1, align=Qt.AlignRight)

    button2 = PushButton('AZ Studio')
    button2.setFixedWidth(120)
    button2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(AZ_URL)))
    view.addWidget(button2, align=Qt.AlignRight)

    button3 = PrimaryPushButton('检查更新')
    button3.setFixedWidth(120)
    button3.clicked.connect(parent.upworker.start)
    view.addWidget(button3, align=Qt.AlignRight)

    # adjust layout (optional)
    view.widgetLayout.insertSpacing(1, 5)
    view.widgetLayout.addSpacing(5)

    # show view
    w = Flyout.make(view, parent.aboutCard, parent)
    view.closed.connect(w.close)

def dlsuc(parent, content, title="", show_time=3000):
    # convenient class mothod
    InfoBar.success(
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=show_time,
        parent=parent)


def dlerr(outid, parent, title="错误", show_time=3000):
    InfoBar.error(
        title=title,
        content=getoutputvalue(outid=outid),
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=show_time,
        parent=parent)


def dlwar(outid, parent, title="警告", show_time=3000):
    InfoBar.warning(
        title=title,
        content=getoutputvalue(outid=outid),
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=show_time,
        parent=parent)
    

def flyout_bottom(parent, title, content, button_content, button_todo, duration=3000):
    w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title=title,
            content=content,
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=duration,
            parent=parent
        )

    s = PushButton(button_content)
    w.addWidget(s)
    s.clicked.connect(button_todo)
    w.show()

def restart(parent):
    w = InfoBar.warning(
        title='',
        content='设置需要重启程序后生效',
        orient=Qt.Vertical,
        position=InfoBarPosition.TOP_RIGHT,
        duration=3000,
        parent=parent
    )
    s = PushButton("立即关闭应用程序")
    w.addWidget(s)
    s.clicked.connect(lambda: exit(0))
    w.show()

def setOK(parent, howto="settings"):
    if howto == "settings":
        content = '设置已保存'
        time = 1500
    elif howto == "playlists":
        content = "导入任务已提交！稍等片刻，歌单就会出现在列表中。"
        time = 2500
    InfoBar.success(
        '',
        content,
        parent=parent,
        duration=time
    )