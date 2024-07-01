import json, AZMusicAPI
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import requests, os
from mutagen.easyid3 import EasyID3
from helper.config import cfg, pfg
from helper.getvalue import download_log, playlist_download_log
from helper.flyoutmsg import dlsuc, dlerr, dlwar
from win11toast import toast

from helper.loggerHelper import logger
from helper.pluginHelper import plugins_api_items

thread = None


class downloading(QThread):
    finished = pyqtSignal(str)

    def __init__(self, howto):
        super().__init__()
        self.howto = howto

    @pyqtSlot()
    def run(self):
        musicpath = cfg.get(cfg.downloadFolder)
        if self.howto == "search":
            u = open(download_log, "r")
        elif self.howto == "playlist":
            u = open(playlist_download_log, "r")

        data = json.loads(u.read())
        u.close()
        id = data["id"]
        if pfg.apicard.value == "NCMA" or pfg.apicard.value == "QQMA":
            api = data["api"]
        song = data["song"]
        singer = data["singer"]

        if pfg.apicard.value == "QQMA" and self.howto == "search":
            url = AZMusicAPI.geturl(id=id, api=api, server="qqma")
        elif pfg.apicard.value == "NCMA" and self.howto == "search":
            url = AZMusicAPI.geturl(id=id, api=api)
        elif self.howto == "search":
            try:
                api_plugin = plugins_api_items[pfg.apicard.value]
                url = api_plugin.geturl(id=id)
            except Exception as e:
                url = "PluginAPIImportError"
                error_msg = e
        else:
            url = AZMusicAPI.geturl(id=id, api=api)
        if url == "Error 3":
            self.show_error = "Error 3"
            self.finished.emit("Error")
        elif url == "Error 4":
            self.show_error = "Error 4"
            self.finished.emit("Error")
        elif url == "NetworkError":
            self.show_error = "NetworkError"
            self.finished.emit("Error")
        elif url == "PluginAPIImportError":
            self.show_error = "PluginAPIImportError"
            if cfg.debug_card.value:
                logger.error(f"插件错误：{error_msg}")
            self.finished.emit("Error")

        if not "Error" in url:
            response = requests.get(url, stream=True)
            file_size = int(response.headers.get('content-length', 0))
            chunk_size = file_size // 100
            path = "{}\\{} - {}.mp3".format(musicpath, singer, song)
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    downloaded_bytes = f.tell()
                    progress = downloaded_bytes * 100 // file_size
                    if downloaded_bytes % chunk_size == 0:
                        self.finished.emit(str(progress))

            self.finished.emit(str(200))


class show_toast(QThread):
    def __init__(self, content, path, musicpath):
        super().__init__()
        self.content = content
        self.path = path
        self.musicpath = musicpath

    def run(self):
        buttons = [
            {'activationType': 'protocol', 'arguments': self.path, 'content': '播放'},
            {'activationType': 'protocol', 'arguments': self.musicpath, 'content': '打开文件夹'}]

        toast('AZMusicDownloader', self.content, buttons=buttons)


class download(QThread):
    def __init__(self, progress, table, progressbar, songdata, dworker, button, parent, howto):
        self.progress = progress
        self.table = table
        self.progressbar = progressbar
        self.songdata = songdata
        self.dworker = dworker
        self.button = button
        self.parent = parent
        self.howto = howto
        self.run()

    def run(self):
        musicpath = cfg.get(cfg.downloadFolder)
        if self.progress == "200":
            self.progressbar.setValue(100)

            if self.howto == "search":
                row = self.table.currentIndex().row()
                try:
                    data = self.songdata[row]
                except:
                    dlwar(outid=2, parent=self.parent)
                    return 0

                song_id = data["id"]
                song = data["name"]
                singer = data["artists"]
                album = data["album"]
                self.dworker.quit()
            elif self.howto == "lists":
                u = open(playlist_download_log, "r")
                data = json.loads(u.read())
                u.close()
                song = data["song"]
                singer = data["singer"]
                album = data["album"]

            self.table.clearSelection()
            self.button.setEnabled(False)
            path = "{}\\{} - {}.mp3".format(musicpath, singer, song)
            path = os.path.abspath(path)

            audio = EasyID3(path)
            audio['title'] = song
            audio['album'] = album
            audio["artist"] = singer
            audio.save()

            self.progressbar.setHidden(True)
            text = '音乐下载完成！\n歌曲名：{}\n艺术家：{}\n保存路径：{}'.format(song, singer, path)
            dlsuc(content=text, parent=self.parent)
            if cfg.toast.value:
                global thread
                thread = show_toast(content=text, path=path, musicpath=musicpath)
                thread.start()
                #thread.wait()
                thread.finished.connect(thread.quit)

        elif self.progress == "Error":
            error = self.dworker.show_error
            self.dworker.quit()
            self.progressbar.setHidden(True)
            self.button.setEnabled(False)
            self.table.clearSelection()

            if error == "Error 3":
                dlerr(outid=7, parent=self.parent)
            elif error == "Error 4":
                dlerr(outid=8, parent=self.parent)
            elif error == "NetworkError":
                dlerr(outid=6, parent=self.parent)
            elif error == "PluginAPIImportError":
                dlerr(9, self.parent)
        else:
            self.progressbar.setValue(int(self.progress))
