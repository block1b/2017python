# coding=utf8
#
import wx
import urllib2, json


class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'post请求发送工具', size=(600, 300))

        bkg = wx.Panel(self)

        la1 = wx.StaticText(bkg, -1)
        la2 = wx.StaticText(bkg, -1)

        font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        la1.SetFont(font)
        la1.SetLabel("url:")
        la2.SetFont(font)
        la2.SetLabel("body:")

        loadButton = wx.Button(bkg, label="发送")
        loadButton.Bind(wx.EVT_BUTTON, self.load)
        self.filename = wx.TextCtrl(bkg, -1, u'http://127.0.0.1:5006/api/push')
        self.contents = wx.TextCtrl(bkg, -1, u'[{"sn": "123456789", "tem": "32.0000"}]', style=wx.TE_MULTILINE | wx.HSCROLL)

        hbox = wx.BoxSizer()
        hbox.Add(la1, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(self.filename, proportion=1, flag=wx.EXPAND)
        hbox.Add(loadButton, proportion=0, flag=wx.LEFT, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(la2, proportion=0, flag=wx.LEFT, border=5)
        vbox.Add(self.contents, proportion=1,
                 flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

        bkg.SetSizer(vbox)

    def OnCloseMe(self, event):
        dlg = wx.MessageDialog(None, u"已发送", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close(True)
        dlg.Destroy()

    def load(self, event):

        # res = urllib2.urlopen(request, timeout=2)  # 打开请求对象，超时
        try:
            url = str(self.filename.GetValue())
            postdata = json.loads(self.contents.GetValue())  # 如何将"[s,s]",转为[s,s]
            # print "url:", url, type(url)
            # print "body:", postdata, type(postdata)
            # url = "http://192.168.1.44:5006/api/push"
            # postdata = [{"sn": "123456789", "hum": "32.0000"}]
            json_data = json.dumps(postdata)  # 此处把没用的0除去了例0.27000变为0.27,并将数据类型转化为字符串。以标准的格式编码（encode）
            request = urllib2.Request(url, json_data)  # 指定额外的数据发送到服务器，数据应该是缓存在一个标准的application/x-www-form-urlencoded格式
            request.add_header('Content-Type', 'application/json')
            request.get_method = lambda: 'POST'  # 服务器允许的请求
            res = urllib2.urlopen(request, timeout=2)  # 打开请求对象，超时
            print "success"
            dlg = wx.MessageDialog(None, u"发送成功！是否继续发送？", u"执行结果", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                pass
            else:
                self.Close(True)
            dlg.Destroy()
        except Exception as e:
            print "error", e
            dlg = wx.MessageDialog(None, u"发送失败!请检查输入的参数", u"执行结果", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                pass
            else:
                self.Close(True)
            dlg.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()