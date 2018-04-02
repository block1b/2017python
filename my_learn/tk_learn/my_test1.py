# coding=utf8
# 前端与后端套路不一样，样例太少。
# 增加参数检查
# 面向对象见mytest2.py

import wx
import urllib2, json


def load(event):
    url = str(filename.GetValue())
    postdata = json.loads(contents.GetValue())  # 如何将"[s,s]",转为[s,s]
    # print "url:", url, type(url)
    # print "body:", postdata, type(postdata)
    # url = "http://192.168.1.44:5006/api/push"
    # postdata = [{"sn": "123456789", "hum": "32.0000"}]
    json_data = json.dumps(postdata)  # 此处把没用的0除去了例0.27000变为0.27,并将数据类型转化为字符串。以标准的格式编码（encode）
    request = urllib2.Request(url, json_data)  # 指定额外的数据发送到服务器，数据应该是缓存在一个标准的application/x-www-form-urlencoded格式
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'POST'  # 服务器允许的请求
    # res = urllib2.urlopen(request, timeout=2)  # 打开请求对象，超时
    try:
        res = urllib2.urlopen(request, timeout=2)  # 打开请求对象，超时
        print "success"
    except Exception as e:
        print "error", e


app = wx.App()

win = wx.Frame(None, title="post请求发送工具", size=(410, 335))
bkg = wx.Panel(win)

la1 = wx.StaticText(bkg, -1)
la2 = wx.StaticText(bkg, -1)

font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
la1.SetFont(font)
la1.SetLabel("url:")
la2.SetFont(font)
la2.SetLabel("body:")

loadButton = wx.Button(bkg, label="发送")
loadButton.Bind(wx.EVT_BUTTON, load)
filename = wx.TextCtrl(bkg, -1, u'http://127.0.0.1:5006/api/push')
contents = wx.TextCtrl(bkg, -1, u'[{"sn": "123456789", "tem": "32.0000"}]', style=wx.TE_MULTILINE | wx.HSCROLL)

hbox = wx.BoxSizer()
hbox.Add(la1, proportion=0, flag=wx.LEFT, border=5)
hbox.Add(filename, proportion=1, flag=wx.EXPAND)
hbox.Add(loadButton, proportion=0, flag=wx.LEFT, border=5)



vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(la2, proportion=0, flag=wx.LEFT, border=5)
vbox.Add(contents, proportion=1,
         flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

bkg.SetSizer(vbox)
win.Show()

app.MainLoop()