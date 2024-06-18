from helper.config import cfg
from helper.inital import mkf
import os

path = cfg.get(cfg.downloadFolder)
mkf()

def get_all_music():
    all_music = []
    path = cfg.get(cfg.downloadFolder)
    for file_name in os.listdir(path):
        if file_name.endswith(".mp3"):
            all_music.append(file_name)
    return all_music