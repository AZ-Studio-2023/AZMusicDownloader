import json, os
from helper.getvalue import apilists
from qfluentwidgets import MessageBoxBase, SubtitleLabel, CheckBox, LineEdit, HyperlinkButton, TransparentPushButton, ToolTipFilter, ToolTipPosition
from PyQt5.QtWidgets import QLabel, QHBoxLayout
from qfluentwidgets import FluentIcon as FIF
from helper.getvalue import autoncmaapi, autoqqmaapi

ncma_edited_api = None
qqma_edited_api = None



def get_all_api(folders_arg):
    global apilists
    for folder in folders_arg:
        for filename in os.listdir(folder):
            last_path = os.path.basename(folder)
            if filename.endswith('.py') and os.path.exists(folder) and os.path.exists(
                    folder + "/index.json") and filename.replace(".py", "") == last_path and not os.path.exists(
                folder + "/plugin.lock"):
                u = open(folder + "/index.json", "r", encoding="utf-8")
                data = json.loads(u.read())
                u.close()
                if data["type"] == "api":
                    apilists.append(data["name"])
    return apilists

class DeleteAllData(MessageBoxBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('重置应用', self)
        self.contentLabel = QLabel("你确定要重置应用吗？\n重置应用将会删除你的设置等数据，\n同时你将会回到初始化时的状态。\n重置后将会直接关闭应用，\n请确保没有任何正在执行的下载任务。", self)
        self.contentLabel.setStyleSheet("QLabel{color:rgb(225,0,0);font-size:17px;font-weight:normal;font-family:SimHei;}")

        self.PrimiseCheckBox = CheckBox('我已悉知以上影响', self)
        self.DataCheckBox = CheckBox('同时删除下载的音乐', self)
        self.DataCheckBox.setDisabled(True)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.contentLabel)
        self.viewLayout.addWidget(self.PrimiseCheckBox)
        self.viewLayout.addWidget(self.DataCheckBox)

        # change the text of button
        self.yesButton.setText('取消')
        self.cancelButton.setText('重置')

        self.widget.setMinimumWidth(350)
        self.cancelButton.setDisabled(True)
        #self.urlLineEdit.textChanged.connect(self._validateUrl)
        self.PrimiseCheckBox.stateChanged.connect(self.IfPrimise)
    
    def IfPrimise(self):
        self.cancelButton.setEnabled(self.PrimiseCheckBox.isChecked())

class CustomAPIs(MessageBoxBase):
    def __init__(self, parent, ncmaapi, qqmaapi):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('自定义NCMA/QQMA的API地址', self)
        self.contentLabel = QLabel("API地址是一个完整的，包含协议头的地址。\nNCMA地址必须填写，QQMA由于没有默认值可以不填。\n填写错误会导致下载失败，有任何问题请查阅文档", self)
        self.contentLabel.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:Microsoft YaHei;}")
        
        # NCMA配置
        self.ncmaLabel = QLabel("NCMA:", self)
        self.ncmaLabel.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:Microsoft YaHei;}")
        self.NCMAedit = LineEdit(self)
        self.NCMAedit.setPlaceholderText('输入NCMA的API地址配置')
        self.NCMAedit.setText(ncmaapi)
        self.NCMAedit.setClearButtonEnabled(True)
        
        self.NCMAtoInit = TransparentPushButton('恢复默认值', self)
        self.NCMAtoInit.setToolTip(f'NCMA的默认值为 {autoncmaapi}')
        self.NCMAtoInit.installEventFilter(ToolTipFilter(self.NCMAtoInit, 0, ToolTipPosition.TOP))
        self.NCMAdoc = HyperlinkButton(
            url='https://md.azprod.cn/docs/use_api.html',
            text='查阅文档',
            parent=self,
            icon=FIF.LINK
        )
        
        self.ncmaHLayout = QHBoxLayout(self)
        self.ncmaHLayout.addWidget(self.NCMAtoInit)
        self.ncmaHLayout.addWidget(self.NCMAdoc)
        
        # QQMA配置
        self.qqmaLabel = QLabel("QQMA:", self)
        self.qqmaLabel.setStyleSheet("QLabel{font-size:15px;font-weight:normal;font-family:SimHei;font-family:Microsoft YaHei;}")
        self.QQMAedit = LineEdit(self)
        self.QQMAedit.setPlaceholderText('输入QQMA的API地址配置')
        self.QQMAedit.setText(qqmaapi)
        self.QQMAedit.setClearButtonEnabled(True)

        self.QQMAtoInit = TransparentPushButton('恢复默认值', self)
        self.QQMAtoInit.setToolTip('QQMA可以不填，同时没有默认值')
        self.QQMAtoInit.installEventFilter(ToolTipFilter(self.QQMAtoInit, 0, ToolTipPosition.TOP))
        self.QQMAdoc = HyperlinkButton(
            url='https://md.azprod.cn/docs/use_api.html',
            text='查阅文档',
            parent=self,
            icon=FIF.LINK
        )
        
        self.qqmaHLayout = QHBoxLayout(self)
        self.qqmaHLayout.addWidget(self.QQMAtoInit)
        self.qqmaHLayout.addWidget(self.QQMAdoc)
        
        # 添加布局
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.contentLabel)
        self.viewLayout.addWidget(self.ncmaLabel)
        self.viewLayout.addWidget(self.NCMAedit)
        self.viewLayout.addLayout(self.ncmaHLayout)
        self.viewLayout.addWidget(self.qqmaLabel)
        self.viewLayout.addWidget(self.QQMAedit)
        self.viewLayout.addLayout(self.qqmaHLayout)

        # 对按钮进行设置
        self.yesButton.setText('保存')
        self.cancelButton.setText('取消')
        self.widget.setMinimumWidth(350)
        self.NCMAtoInit.clicked.connect(self.ncmabacktoinit)
        self.QQMAtoInit.clicked.connect(self.qqmabacktoinit)
        self.yesButton.clicked.connect(self.save)
    
    def ncmabacktoinit(self):
        self.NCMAedit.setText(autoncmaapi)
    def qqmabacktoinit(self):
        self.QQMAedit.setText(autoqqmaapi)
        
    def save(self):
        # 设置修改操作
        global ncma_edited_api
        global qqma_edited_api
        ncma_edited_api = self.NCMAedit.text()
        qqma_edited_api = self.QQMAedit.text()
        
def editapi(parent, ncmaapi, qqmaapi):
    w = CustomAPIs(parent=parent, ncmaapi=ncmaapi, qqmaapi=qqmaapi)
    w.show()
    if w.exec():
        new_api = []
        new_api.append(ncma_edited_api)
        new_api.append(qqma_edited_api)
        return new_api
    else:
        w = False
        