from helper.inital import mkf
from helper.getvalue import localView
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from PyQt5.QtWidgets import QTableWidgetItem
import subprocess
from os import listdir
from os.path import join, isfile

mkf()


def get_all_music(path):
    all_music = []
    for file_name in listdir(path):
        file_path = f"{path}\{file_name}"
        if isfile(file_path):
            all_music.append(file_name)
    return all_music


def ref(musicpath, local_view=None):
    global localView
    if local_view:
        localView = local_view
    if not local_view:
        local_view = localView
    local_view.clear()
    local_view.setHorizontalHeaderLabels(['文件名', '歌曲名', '艺术家', '专辑'])

    data = get_all_music(path=musicpath)
    songInfos = []
    for stand in data:
        path = join(musicpath, stand)
        try:
            audio = EasyID3(path)
        except ID3NoHeaderError:
            continue
        songinfo = [stand]
        try:
            songinfo.append(audio['title'][0])
        except KeyError:
            songinfo.append("Unknown")
        try:
            songinfo.append(audio['artist'][0])
        except KeyError:
            songinfo.append("Unknown")
        try:
            songinfo.append(audio['album'][0])
        except KeyError:
            songinfo.append("Unknown")
        songInfos.append(songinfo)

    local_view.setRowCount(len(songInfos))

    for i, songInfo in enumerate(songInfos):
        for j, info in enumerate(songInfo):
            local_view.setItem(i, j, QTableWidgetItem(info))


def openthemusic(filepath):
    global localView
    row = localView.currentIndex().row()
    data = get_all_music(path=filepath)
    name = data[row]
    file_path = join(filepath, name)
    cmd = f'start "" "{file_path}"'
    localView.clearSelection()
    subprocess.Popen(cmd, shell=True)
