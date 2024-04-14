import winreg

def _init():
    global musicpath
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    documents_path_value = winreg.QueryValueEx(reg_key, "My Music")
    musicpath = documents_path_value[0]