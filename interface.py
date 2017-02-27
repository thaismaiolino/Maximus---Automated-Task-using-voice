import Tkinter as tk
import ttk


LARGE_FONT= ("Verdana", 12)

class Interface(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container["padx"] = 200
        container["pady"] = 50

        self.frames = {}

        for F in (StartPage, SettingsPage, ExcludePage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.exit = tk.Button(self, text="Sair", font=LARGE_FONT, width=12)
        self.exit["command"] = self.quit

        self.btnListing = tk.Button(self, text="Ouvir", font=LARGE_FONT, width=12)
        self.btnListing["command"] = self.doSomething


        self.btnInfo = tk.Button(self, text="Settings", font=LARGE_FONT, width=12 , command=lambda: controller.show_frame(SettingsPage))


        self.msg = tk.Label(self, text="Primeiro widget")
        self.msg["font"] = ("Calibri", "9", "italic")
        self.msg.pack ()

        self.btnInfo.pack ()
        self.btnListing.pack ()
        self.exit.pack ()

