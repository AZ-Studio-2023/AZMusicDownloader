from datetime import date
from random import randint
from PyQt5.QtCore import QStandardPaths
import ctypes

config_path_value = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
allpath = "{}\\AZMusicDownload".format(config_path_value)
playlistpath = "{}\\playlists.json".format(allpath)

configpath = "{}\\config.json".format(allpath)
upurl = "https://json.zenglingkun.cn/update/md/index.json"

music_path_value = QStandardPaths.writableLocation(QStandardPaths.MusicLocation)
autopath = "{}\\AZMusicDownload".format(music_path_value)
localView = None

autoncmaapi = "https://ncma.azprod.cn/"  # API为ncma的克隆项目
autoqqmaapi = ""
apilists = ['NCMA', 'QQMA']
playlistSong = ""
searchSong = ""
download_search_song = ""
download_playlist_song = ""

# 古诗
poem = ["天阶夜色凉如水，卧看牵牛织女星。",
        "唯有门前镜湖水，春风不改旧时波。",
        "三更灯火五更鸡，正是男儿读书时。",
        "但屈指西风几时来，又不道流年暗中偷换。",
        "俱往矣，数风流人物，还看今朝。",
        "水是眼波横，山是眉峰聚。",
        "明年此日青云去，却笑人间举子忙。",
        "衰兰送客咸阳道，天若有情天亦老。",
        "昔去雪如花，今来花似雪。",
        "青青子衿，悠悠我心。",
        "执子之手，与子偕老。",
        "老来情味减，对别酒、怯流年。",
        "什么是时光？我们穿上的衣服，却再也脱不下来。",
        "但行好事，莫问前程。",
        "吾道本无我，未曾嫌世人。如今到尘世，弥觉此心真",
        "去年今日此门中，人面桃花相映红。",
        "似花还似非花，也无人惜从教坠。",
        "墙外行人，墙里佳人笑。",
        "海内存知己，天涯若比邻。",
        "七八个星天外，两三点雨山前。"]


def outapoem():
    outpoem = poem[randint(0, len(poem) - 1)]
    return outpoem


def GetDefaultThemeColor():
    dwmapi = ctypes.windll.dwmapi
    color = ctypes.c_ulong()
    opaque = ctypes.c_bool()

    # Call DwmGetColorizationColor
    result = dwmapi.DwmGetColorizationColor(ctypes.byref(color), ctypes.byref(opaque))

    if result == 0:  # S_OK
        # Extract the color components (ARGB format)
        alpha = (color.value >> 24) & 0xFF
        red = (color.value >> 16) & 0xFF
        green = (color.value >> 8) & 0xFF
        blue = color.value & 0xFF

        return (f"#{red:02X}{green:02X}{blue:02X}")
    else:
        return ("#0078D4")


# 错误内容列表
outputlist = ['未搜索到相关的歌曲，换个关键词试试吧',
              '你还没有输入噢',
              '您选中的行无数据',
              '音乐下载路径无法读取\创建失败',
              "未配置NeteaseCloudMusicApi地址",
              "未配置QQMusicApi地址",
              '您可能是遇到了以下其一问题：网络错误 / 服务器宕机 / IP被封禁',
              '这首歌曲无版权，暂不支持下载',
              '获取链接失败，建议检查API服务器是否配置了账号Cookie',
              '插件未成功导入，请检查插件']

verdetail = "1.更改歌单保存方式\n2.优化逻辑\n由于歌单保存方式改变，请您更新前备份好您的歌单数据"

# 全局变量处理
def get_download_search_song():
    global download_search_song
    return download_search_song

def set_download_search_song(value):
    global download_search_song
    download_search_song=value

def get_download_playlist_song():
    global download_playlist_song
    return download_playlist_song

def set_download_playlist_song(value):
    global download_playlist_song
    download_playlist_song=value


YEAR = int(date.today().year)
AUTHOR = "AZ Studio"
VERSION = "2.6.5"
UPDATE_ORDER = 14
HELP_URL = "https://md.azprod.cn/docs/"
FEEDBACK_URL = "https://github.com/AZ-Studio-2023/AZMusicDownloader/issues"
RELEASE_URL = "https://github.com/AZ-Studio-2023/AZMusicDownloader/releases/tag/v2.6.5"
AZ_URL = "https://azstudio.net.cn/"
PLU_URL = "https://plugins.md.azprod.cn/"
SERVER_URL = "https://www.lcyidc.com/"
