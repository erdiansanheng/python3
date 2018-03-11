# -*- coding: utf-8 -*-

import wx

app = wx.App()

frame = wx.Frame(None, -1, title = 'Hello World', pos = (300, 400), size = (500,400))
#frame.Centre()
frame.Show()

print('Hi!') #App()参数为True时，print()的内容；另起窗口输出窗口内

app.MainLoop()