from PyQt5.QtWidgets import QApplication, QSplashScreen
from window.main import Window
from sys import argv
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from helper.resource import _init

if __name__ == '__main__':
    _init()
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(argv)
    splash_pix = QPixmap('resource/MusicDownloader.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setAttribute(Qt.WA_TranslucentBackground)
    splash.show()
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
    splash_width = 1313
    splash_height = 736
    splash.setFixedSize(splash_width, splash_height)
    splash.move((screen_width - splash_width) // 2, (screen_height - splash_height) // 2)
    app.processEvents()
    w = Window()
    w.show()
    splash.finish(w)
    app.exec_()
