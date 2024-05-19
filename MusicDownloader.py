from PyQt5.QtWidgets import QApplication, QSplashScreen
from qfluentwidgets import FluentTranslator
from helper.config import cfg
from window.main import Window
import sys
from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QPixmap
from win32api import MessageBox
from win32con import MB_ICONHAND
from helper.inital import mkf

def global_exception_handler(exc_type, exc_value, exc_traceback):
    msesg = str(exc_type) + str(exc_value) + str(exc_traceback)
    MessageBox(0, msesg, "请将这个错误反馈给我们", MB_ICONHAND)
sys.excepthook = global_exception_handler

if __name__ == '__main__' and sys.platform == 'win32' and sys.getwindowsversion().build >= 7601:
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    mkf()
    
    splash_pix = QPixmap('resource/splash.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setAttribute(Qt.WA_TranslucentBackground)
    splash.show()
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
    splash_width = 283
    splash_height = 276
    splash.setFixedSize(splash_width, splash_height)
    splash.move((screen_width - splash_width) // 2, (screen_height - splash_height) // 2)
    
    locale = cfg.get(cfg.language).value
    fluentTranslator = FluentTranslator(locale)
    settingTranslator = QTranslator()
    settingTranslator.load(locale, "settings", ".", "resource/i18n")

    app.installTranslator(fluentTranslator)
    app.installTranslator(settingTranslator)
    app.processEvents()
    
    w = Window()
    w.show()
    splash.finish(w)
    app.exec_()
else:
    text = "不支持的操作系统：" + sys.platform
    MessageBox(0, text, "软件启动错误", MB_ICONHAND)