import json
from os import path, makedirs, remove
from helper.config import cfg
from helper.getvalue import (apipath, download_log, search_log, autoapi, configpath,
                             playlistpath, logpath, playlist_download_log, playlist_search_log)


def mkf():
    dlpath = cfg.get(cfg.downloadFolder)
    if not path.exists(logpath):
        makedirs(logpath)
    if not path.exists(download_log):
        d = open(download_log, "w")
        d.close()
    if not path.exists(playlist_download_log):
        d = open(playlist_download_log, "w")
        d.close()
    if not path.exists(playlist_search_log):
        d = open(playlist_search_log, "w")
        d.close()
    if not path.exists(search_log):
        d = open(search_log, "w")
        d.close()
    if not path.exists(apipath):
        u = open(apipath, "w")
        u.write(json.dumps({"api": autoapi}))
        u.close()
    if not path.exists(dlpath):
        makedirs(dlpath)
    if not path.exists(playlistpath):
        makedirs(playlistpath)
        
def delfin():
    if path.exists(configpath):
        remove(configpath)
    if path.exists(playlist_download_log):
        remove(playlist_download_log)
    if path.exists(playlist_search_log):
        remove(playlist_search_log)
    if path.exists(download_log):
        remove(download_log)
    if path.exists(apipath):
        remove(apipath)
    if path.exists(search_log):
        remove(search_log)