from Tkinter import *
import appDb as db


global nickname
global user

nickname = db.returnDocUser()["callname"]
user = db.returnDocUser()['user']

class SettingsPage(object):

    def __init__(self,window):
        self.window = window
        self.window.wm_title("Settings")

        l0=Label(window,text="Your Name:")
        l0.grid(row=0,column=0)

        self.name_text=StringVar()
        self.e0=Entry(window,textvariable=self.name_text)
        self.e0.insert(0, user )
        self.e0.grid(row=0,column=1)


        l1=Label(window,text="Machine nickname:")
        l1.grid(row=1,column=0)

        self.machine_name_text=StringVar()
        self.e1=Entry(window,textvariable=self.machine_name_text)
        self.e1.insert(0, nickname )
        self.e1.grid(row=1,column=1)

        b1=Button(window,text="Save", width=12,command=self.view_command)
        b1.grid(row=3,column=1)


        b2=Button(window,text="Close", width=12,command=window.destroy)
        b2.grid(row=3,column=0)




    def view_command(self):
        if self.name_text.get() == user and self.machine_name_text.get() == nickname:
            print 'There is no changes to be saved.'
            l2=Label(window,text="There is no changes to be saved.", fg="red")
            l2.grid(row=2,column=0)
        else:
            db.removeProfile()
            db.addProfile(self.name_text.get(), self.machine_name_text.get())

            global nickname
            nickname = db.returnDocUser()["callname"]

            global user
            user = db.returnDocUser()['user']
            l2=Label(window,text="Information Saved!",fg="red")
            l2.grid(row=2,column=0)


window=Tk()
SettingsPage(window)
window.mainloop()
