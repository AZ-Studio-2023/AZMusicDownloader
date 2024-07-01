# coding:utf-8
import importlib, sys, json, os
from qfluentwidgets import SwitchSettingCard, PushSettingCard
from helper.config import cfg
from helper.flyoutmsg import dlerr
from helper.loggerHelper import logger
from qfluentwidgets import FluentIcon as FIF

plugins_items = {}
plugins_api_items = {}
folders = cfg.PluginFolders.value


def get_folders(directory):
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folders.append(item)
    return folders


def load_plugins(parent):
    global plugins_items
    global plugins_api_items
    # 遍历插件目录中的文件
    num = 0
    if cfg.debug_card.value:
        logger.info("开始导入插件")
    for dirname in folders:
        sys.path.append(dirname)
        for filename in os.listdir(dirname):
            last_path = os.path.basename(dirname)
            if filename.endswith('.py') and os.path.exists(dirname) and os.path.exists(
                    dirname + "/index.json") and filename.replace(".py", "") == last_path and not os.path.exists(
                    dirname + "/plugin.lock"):
                plugin_name = filename[:-3]
                module_name = f"{plugin_name}"
                try:
                    module = importlib.import_module(module_name)
                    plugin_class = getattr(module, plugin_name)
                    u = open(dirname + "/index.json", encoding='utf-8')
                    data = json.loads(u.read())
                    u.close()
                    if data["type"] == "api":
                        plugins_api_items[data["name"]] = plugin_class()
                    plugins_items[plugin_name] = plugin_class()
                    if cfg.debug_card.value:
                        logger.info(f"导入插件: {plugin_name}")
                    num = num + 1
                except Exception as e:
                    logger.error(f"导入{plugin_name}插件错误: {e}")
    #if cfg.debug_card.value:
    #    print("添加Plugins中的API")
    #get_all_api()
    if cfg.debug_card.value:
        logger.info(f"成功导入了{str(num)}个插件")


def run_plugins(parent):
    global plugins_items
    num = 0
    for plugin_name, plugin_instance in plugins_items.items():
        folder = folders[num]
        num = num + 1
        get_v = open(f"{folder}/index.json", "r", encoding="utf-8")
        data = json.loads(get_v.read())
        get_v.close()
        if data["type"] == "Bar" and os.path.basename(folder) == plugin_name:
            #icon = f'plugins/{plugin_name}/{data["icon"]}'
            icon = data["show_icon"]
            #icon = "resource/logo.png"
            name = data["name"]
            logger.debug(f"将插件添加至导航栏: {plugin_name}")
            exec(f"parent.addSubInterface(plugin_instance, {icon}, '{name}')")


def set_plugin_disable(folder, state):
    if not state:
        w = open(f"{folder}/plugin.lock", "w")
        w.close()
    else:
        if os.path.exists(f"{folder}/plugin.lock"):
            os.remove(f"{folder}/plugin.lock")


def run_plugins_plugin(parent, PluginsGroup):
    folders = cfg.PluginFolders.value
    for folder in folders:
        if os.path.exists(folder + "/index.json"):
            get_json = open(f"{folder}/index.json", "r", encoding="utf-8")
            data = json.loads(get_json.read())
            get_json.close()
            addCard(parent, PluginsGroup, data["icon"], data["name"], data["desc"], data["type"], folder)


def open_plugin_window(plugin, parent):
    try:
        plugin_name = os.path.basename(plugin)
        new = plugins_items[plugin_name]
        if os.path.exists(plugin + "/index.json"):
            get_json = open(f"{plugin}/index.json", "r", encoding="utf-8")
            data = json.loads(get_json.read())
            new.setWindowTitle(data["name"])
        new.show()
    except Exception as e:
        dlerr(outid=9, parent=parent)
        if cfg.debug_card.value:
            logger.error(f"插件错误：{e}")


def addCard(parent, PluginsGroup, icon, title, content, type, uuid):
    if type == "Bar":
        PluginCard_Bar = SwitchSettingCard(
            icon,
            title,
            content,
            None,
            PluginsGroup
        )
        PluginCard_Bar.checkedChanged.connect(lambda: set_plugin_disable(uuid, PluginCard_Bar.isChecked()))
        if not os.path.exists(uuid + "/plugin.lock"):
            PluginCard_Bar.setValue(True)
        else:
            PluginCard_Bar.setValue(False)
        PluginCard_Bar.setObjectName(os.path.basename(uuid))
        parent.PluginsGroup.addSettingCard(PluginCard_Bar)
    elif type == "api":
        PluginCard_api = SwitchSettingCard(
            icon,
            title,
            content,
            None,
            PluginsGroup
        )
        PluginCard_api.checkedChanged.connect(lambda: set_plugin_disable(uuid, PluginCard_api.isChecked()))
        if not os.path.exists(uuid + "/plugin.lock"):
            PluginCard_api.setValue(True)
        else:
            PluginCard_api.setValue(False)
        PluginCard_api.setObjectName(os.path.basename(uuid))
        parent.PluginsGroup.addSettingCard(PluginCard_api)
    elif type == "Window":
        PluginCard_window = PushSettingCard(
            '打开',
            icon,
            title,
            content,
            PluginsGroup
        )
        PluginCard_window.setObjectName(os.path.basename(uuid))
        PluginCard_window.clicked.connect(lambda: open_plugin_window(uuid, parent=parent))
        parent.PluginsGroup.addSettingCard(PluginCard_window)
