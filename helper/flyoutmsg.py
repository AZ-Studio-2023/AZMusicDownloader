from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition

def dlsuc(content, parent, title = "", show_time = 3000):
    # convenient class mothod
    InfoBar.success(
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=show_time,
        parent=parent)

def dlerr(content, parent, title = "错误", show_time = 3000):
    InfoBar.error(
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=show_time,
        parent=parent)
    
def dlwar(content, parent, title = "警告", show_time = 3000):
    InfoBar.warning(
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=True, 
        position=InfoBarPosition.TOP,
        duration=show_time,
        parent=parent)