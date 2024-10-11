import os
import tempfile
import time
import webbrowser

import requests
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot

from helper.config import cfg


class WorkerSignals(QObject):
    progress = pyqtSignal(int)

class UserLogin(QRunnable):
    def __init__(self):
        super(UserLogin, self).__init__()
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        key = requests.get(cfg.ncma_api.value + f"login/qr/key?timestamp={int(time.time())}").json()["data"]["unikey"]
        img = requests.get(cfg.ncma_api.value + f"login/qr/create?key={key}&qrimg=1&timestamp={int(time.time())}").json()["data"]["qrimg"]
        html_code = f"""
        <!DOCTYPE html>
        <html lang="CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login</title>
        </head>
        <body>
            <img src="{img}">
        </body>
        </html>
        """

        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_file:
            temp_file.write(html_code.encode('utf-8'))
            temp_file_path = temp_file.name

        webbrowser.open(f'file://{temp_file_path}')
        t = 0
        while True:
            d = requests.get(cfg.ncma_api.value + f"login/qr/check?key={key}&timestamp={int(time.time())}").json()
            if d["code"] == 803:
                cfg.set(cfg.cookie, d["cookie"])
                self.signals.progress.emit(200)
                break
            elif d["code"] == 800:
                self.signals.progress.emit(100)
                break
            time.sleep(1)
            t = t + 1
            if t == 5:
                os.remove(temp_file_path)