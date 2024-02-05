from PyQt5.QtWidgets import QApplication, QSplashScreen
from window.main import Window
from sys import argv, exit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(argv)
    splash_pix = QPixmap('resource/MusicDownloader.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setAttribute(Qt.WA_TranslucentBackground)
    splash.show()
    app.processEvents()
    w = Window()
    w.show()
    splash.finish(w)
    app.exec_()
