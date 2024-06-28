from PyQt5.QtWidgets import QApplication, QSplashScreen, QMessageBox, QWidget
from qfluentwidgets import FluentTranslator
from helper.config import cfg
from window.main import Window
import sys
from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QPixmap
from helper.inital import mkf

if not cfg.debug_card.value:
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        msesg = '{}\n{}\n{}'.format(str(exc_type), str(exc_value), str(exc_traceback))
        QMessageBox.critical(w, "There's an error ! ! !", msesg, QMessageBox.Yes)
    sys.excepthook = global_exception_handler

if __name__ == '__main__' and sys.platform == 'win32' and sys.getwindowsversion().build >= 17763:
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    
    splash_pix = QPixmap('resource/splash.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setAttribute(Qt.WA_TranslucentBackground)
    splash.show()
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
    splash_width = 260
    splash_height = 260
    splash.setFixedSize(splash_width, splash_height)
    splash.move((screen_width - splash_width) // 2, (screen_height - splash_height) // 2)

    mkf()

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
    app = QApplication(sys.argv)
    w = QWidget()
    text = "Unsupported operating system: " + sys.platform
    QMessageBox.critical(w, "There is an error when the Application is starting !", text, QMessageBox.Yes)