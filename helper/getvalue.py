import winreg
from datetime import date
from random import randint

reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")

config_path_value = winreg.QueryValueEx(reg_key, "AppData")
DataPath = config_path_value[0]
allpath = "{}\\AZMusicDownload".format(DataPath)
logpath = "{}\\log".format(allpath)
playlistpath = "{}\\playlist".format(allpath)

configpath = "{}\\config.json".format(allpath)
apipath = "{}\\api.json".format(allpath)

download_log = "{}\\download_log.json".format(logpath)
search_log = "{}\\search_log.json".format(logpath)
playlist_download_log = "{}\\playlist_download_log.json".format(logpath)
playlist_search_log = "{}\\playlist_search_log.json".format(logpath)

music_path_value = winreg.QueryValueEx(reg_key, "My Music")
personalmusicpath = music_path_value[0]
autopath = "{}\\AZMusicDownload".format(personalmusicpath)

autoapi = "https://ncma.azprod.cn/"  # API为ncma的克隆项目
upurl = "https://json.zenglingkun.cn/update/md/index.json"

# 古诗
poem =  ["天阶夜色凉如水，卧看牵牛织女星。", 
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

# 错误内容列表
outputlist = ['未搜索到相关的歌曲，换个关键词试试吧',
           '你还没有输入噢',
           '您选中的行无数据', 
           '音乐下载路径无法读取\创建失败', 
           "未配置NeteaseCloudMusicApi地址", 
           "未配置QQMusicApi地址",
           '您可能是遇到了以下其一问题：网络错误 / 服务器宕机 / IP被封禁',
           '这首歌曲无版权，暂不支持下载',
           '获取链接失败，建议检查API服务器是否配置了账号Cookie']

verdetail = "1.优化项目结构，UI与逻辑分离\n2.支持Windows系统通知\n3.修复了部分歌单的已知Bug"

YEAR = int(date.today().year)
AUTHOR = "AZ Studio"
VERSION = "2.5.2"
HELP_URL = "https://md.azprod.cn/docs/"
FEEDBACK_URL = "https://github.com/AZ-Studio-2023/AZMusicDownloader/issues"
RELEASE_URL = "https://github.com/AZ-Studio-2023/AZMusicDownloader/releases/tag/v2.5.2"
AZ_URL = "https://azstudio.net.cn/"
