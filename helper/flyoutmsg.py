from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition

def dlsuc(content, parent):
    # convenient class mothod
    InfoBar.success(
        title="",
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=3000,
        parent=parent)

def dlerr(content, parent):
    InfoBar.error(
        title="错误",
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=3000,
        parent=parent)
    
def dlwar(content, parent):
    InfoBar.warning(
        title="警告",
        content=content,
        orient=Qt.Horizontal,
        isClosable=True, 
        position=InfoBarPosition.TOP,
        duration=3000,
        parent=parent)