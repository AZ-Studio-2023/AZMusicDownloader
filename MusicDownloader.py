from PyQt5.QtWidgets import QApplication
from window.main import Window
from sys import argv, exit
from PyQt5.QtCore import Qt


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(argv)
    w = Window()
    w.show()
    app.exec_()