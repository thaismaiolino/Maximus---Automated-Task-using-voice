import wx
import appDb as db

global nickname
global user

nickname = db.returnDocUser()["callname"]
user = db.returnDocUser()['user']

class SettingsInterface(wx.Frame):

    def __init__(self, parent, title):
        super(SettingsInterface, self).__init__(parent, title=title,
            size=(370, 220))
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 5)

        text1 = wx.StaticText(panel, label="User Settings")
        sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM,
            border=15)

        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('settings-3.png'))
        sizer.Add(icon, pos=(0, 3), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT,
            border=5)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 5),
            flag=wx.EXPAND|wx.BOTTOM, border=10)

        name = wx.StaticText(panel, label="Your Name:")
        sizer.Add(name, pos=(2, 0), flag=wx.LEFT, border=10)

        self.name_tc = wx.TextCtrl(panel, value=user)
        sizer.Add(self.name_tc, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND)

        machine = wx.StaticText(panel, label="Machine Nickname:")
        sizer.Add(machine, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

        self.machine_tc = wx.TextCtrl(panel, value=nickname)
        sizer.Add(self.machine_tc, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND,
            border=5)


        help_btn = wx.Button(panel,wx.ID_INFO, label='Help')
        sizer.Add(help_btn, pos=(5, 0), flag=wx.LEFT, border=10)
        self.Bind(wx.EVT_BUTTON, self.help, id=wx.ID_INFO)

        save_btn = wx.Button(panel,wx.ID_SAVE, label="Save")
        sizer.Add(save_btn, pos=(5, 2))
        self.Bind(wx.EVT_BUTTON, self.SaveChanges, id=wx.ID_SAVE)

        close_btn = wx.Button(panel, wx.ID_EXIT, label="Close")
        sizer.Add(close_btn, pos=(5, 3), span=(1, 1),
            flag=wx.BOTTOM|wx.RIGHT, border=5)

        self.Bind(wx.EVT_BUTTON, self.OnQuitApp, id=wx.ID_EXIT)

        sizer.AddGrowableCol(2)

        panel.SetSizer(sizer)
    def OnQuitApp(self, event):

        self.Close()



    def SaveChanges(self,event):

        if self.name_tc.GetValue() == user and self.machine_tc.GetValue() == nickname:
            self.ShowMessage('There is no changes to be saved.', 'Failed')
        else:
            db.removeProfile()
            db.addProfile(self.name_tc.GetValue(), self.machine_tc.GetValue())

            global nickname
            nickname = db.returnDocUser()["callname"]

            global user
            user = db.returnDocUser()['user']
            self.ShowMessage('Information Saved!', 'Success')

    def help(self):
        pass

    def ShowMessage(self, msg, header):
        wx.MessageBox(msg, header,
            wx.OK | wx.ICON_INFORMATION)

class MyApp(wx.App):
    def OnInit(self):
        frame = SettingsInterface(None, title="Settings")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


def start():
    app = MyApp(0)
    app.MainLoop()


#----------------------------------------------------------------------

overview = __doc__

