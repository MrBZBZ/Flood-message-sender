import keyboard
import wx
import threading
from time import sleep
from pyperclip import copy

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.isRunning = False

        panel = wx.Panel(self)
        self.filePath = wx.TextCtrl(panel, style=wx.TE_LEFT)
        self.shuapin = wx.StaticText(panel,label="当选择普通刷屏模式时请在此输入你要发送的话")
        self.shuapin_input = wx.TextCtrl(panel)
        self.txt = wx.StaticText(panel,label="以下是词汇文件的路径，请先读取txt格式的词汇文件↓↓↓\n如果是普通刷屏模式则不需要读取txt")
        self.txt_1 = wx.StaticText(panel, label="请选择消息发送的按键，默认为Crtl+Enter ↓↓↓")
        self.result = wx.StaticText(panel, label="", style=wx.ALIGN_LEFT)
        btnLoadFile = wx.Button(panel, label="加载词汇")
        btnLoadFile.Bind(wx.EVT_BUTTON, self.onLoadFile)

        ways = ['词汇刷屏', '@人刷屏','普通刷屏']
        ways_1 = ['Ctrl+Enter','Enter']
        self.wayChoice_1 = wx.Choice(panel, choices=ways_1)
        self.wayChoice = wx.Choice(panel, choices=ways)
        self.wayChoice.SetSelection(0)
        self.wayChoice_1.SetSelection(0)

        self.nameText = wx.TextCtrl(panel, style=wx.TE_LEFT, value="如果选择@人，此处直接填写ID")
        self.time = wx.StaticText(panel,label="请在下方输入发送时间间隔")
        self.input = wx.TextCtrl(panel)
        self.nameText.Bind(wx.EVT_SET_FOCUS, self.onFocus)
        self.nameText.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)

        self.startButton = wx.Button(panel, label="开始")
        self.startButton.Bind(wx.EVT_BUTTON, self.onStart)

        self.stopButton = wx.Button(panel, label="停止")
        self.stopButton.Bind(wx.EVT_BUTTON, self.onStop)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.txt,0,wx.ALL,10)
        sizer.Add(self.filePath, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btnLoadFile, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.wayChoice, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.txt_1, 0, wx.ALL, 10)
        sizer.Add(self.wayChoice_1, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.nameText, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.shuapin, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.shuapin_input, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.time, 0,wx.ALL | wx.CENTER,5)
        sizer.Add(self.input, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.startButton, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.result, 0, wx.EXPAND | wx.ALL, 0)
        sizer.Add(self.stopButton, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(sizer)

    def onLoadFile(self, event):
        openFileDialog = wx.FileDialog(self, "打开", "", "", "文本文件 (*.txt)|*.txt",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        self.filePath.SetValue(openFileDialog.GetPath())

    def onFocus(self, event):
        if self.nameText.GetValue() == "如果选择@人，此处直接填写ID":
            self.nameText.SetValue("")
        event.Skip()

    def onKillFocus(self, event):
        if not self.nameText.GetValue():
            self.nameText.SetValue("如果选择@人，此处直接填写ID")
        event.Skip()

    def onStart(self, event):
        self.result.SetLabel("开始发送消息……")
        self.result.SetLabel("开始发送消息……")
        self.isRunning = True
        threading.Thread(target=self.startSending).start()

    def startSending(self):
        ways = self.wayChoice.GetString(self.wayChoice.GetSelection())
        sleep(2)
        if ways == "词汇刷屏":
            self.autoSend(None)
        elif ways == "@人刷屏":
            name = self.nameText.GetValue()
            if name and name != "如果选择@人，此处直接填写ID":
                self.autoSend(name)
            else:
                wx.CallAfter(wx.MessageBox, "请输入你要@的人的ID", "提示", wx.OK | wx.ICON_WARNING)
        else:
            while True:
                if not self.isRunning:
                    break
                copy(self.shuapin_input.GetValue())
                self.pasteAndSend()

    def onStop(self, event):
        self.result.SetLabel("已停止发送消息")
        self.isRunning = False

    def autoSend(self, name):
        with open(self.filePath.GetValue(), 'r') as file:
            if name:
                for line in file:
                    if not self.isRunning:
                        break
                    copy("@" + name + " " + line.strip())
                    self.pasteAndSend()
            else:
                for line in file:
                    if not self.isRunning:
                        break
                    copy(line.strip())
                    self.pasteAndSend()

    def pasteAndSend(self):
        sleep(float(self.input.GetValue()))

        # 模拟 Ctrl + V
        keyboard.press('ctrl')
        keyboard.press('v')
        keyboard.release('v')
        keyboard.release('ctrl')

        sleep(float(self.input.GetValue()))

        send_choice = self.wayChoice_1.GetString(self.wayChoice_1.GetSelection())
        if send_choice == "Enter":
            keyboard.press('enter')
            keyboard.release('enter')
        else:
            # 模拟 Ctrl + Enter
            keyboard.press('ctrl')
            keyboard.press('enter')
            keyboard.release('enter')
            keyboard.release('ctrl')

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, title="洪水扣字器", size=(500, 600))
    frame.Show(True)
    app.MainLoop()