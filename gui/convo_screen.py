import tkinter as tk

TITLE_FONT = ("Black chancery", "18", "bold")
TEXT_FONT = ("Black chancery", "15")
BUTTON_FONT = ("Black chancery", "13")


# TODO enable conversation menus!
class convo_controller(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid()

        self.frames = {}

        for keyboard in (options, topic, store, manu, friend):
            page_name = keyboard.__name__
            frame = keyboard(parent=self, controller=self, root=root)
            self.frames[page_name] = frame


class options(tk.Frame):
    def __init__(self, parent, root, controller):
        tk.Frame.__init__(self, parent)
        self.root = root
        self.controller = controller
        self.hotkeys = []

        header = tk.Label(self, text="Convo Options", font=TITLE_FONT)
        sleep_var = tk.IntVar()
        sleep = tk.Checkbutton(self, text="Sleep", font=TEXT_FONT, variable=sleep_var, command=self.set_convos)
        work_var = tk.IntVar()
        work = tk.Checkbutton(self, text="Work", font=TEXT_FONT, variable=work_var, command=self.set_convos)
        rest_var = tk.IntVar()
        rest = tk.Checkbutton(self, text="Rest", font=TEXT_FONT, variable=rest_var, command=self.set_convos)
        shop_var = tk.IntVar()
        shop = tk.Checkbutton(self, text="Shop", font=TEXT_FONT, variable=shop_var, command=self.set_convos)

        header.pack()
        sleep.pack()
        work.pack()
        rest.pack()
        shop.pack()

    def raise_frame(self):
        self.tkraise()

    def set_convos(self):
        pass


class topic(tk.Frame):
    def __init__(self, parent, root, controller):
        tk.Frame.__init__(self, parent)
        self.root = root
        self.controller = controller
        self.hotkeys = []

        header = tk.Label(self, text="Topic", font=TITLE_FONT)
        stores = tk.Button(self, text="Stores", font=BUTTON_FONT)
        manu = tk.Button(self, text="Manufacturers", font=BUTTON_FONT)
        friends = tk.Button(self, text="Friends", font=BUTTON_FONT)
        end = tk.Button(self, text="End Conversation", font=BUTTON_FONT)

        header.pack()
        stores.pack()
        manu.pack()
        friends.pack()
        end.pack()

    def raise_frame(self):
        self.tkraise()


class store(tk.Frame):
    def __init__(self, parent, root, controller):
        tk.Frame.__init__(self, parent)
        self.root = root
        self.controller = controller
        self.hotkeys = []

        header = tk.Label(self, text="Store", font=TITLE_FONT)
        prices = tk.Button(self, text="Prices", font=BUTTON_FONT)
        different = tk.Button(self, text="Switch Stores", font=BUTTON_FONT)
        topic = tk.Button(self, text="Change Topic", font=BUTTON_FONT)
        end = tk.Button(self, text="End Conversation", font=BUTTON_FONT)

        header.pack()
        prices.pack()
        different.pack()
        topic.pack()
        end.pack()

    def raise_frame(self):
        self.tkraise()


class manu(tk.Frame):
    def __init__(self, parent, root, controller):
        tk.Frame.__init__(self, parent)
        self.root = root
        self.controller = controller
        self.hotkeys = []

        header = tk.Label(self, text="Manufacturer", font=TITLE_FONT)
        prices = tk.Button(self, text="Prices", font=BUTTON_FONT)
        different = tk.Button(self, text="Switch Manufacturers", font=BUTTON_FONT)
        topic = tk.Button(self, text="Change Topic", font=BUTTON_FONT)
        end = tk.Button(self, text="End Conversation", font=BUTTON_FONT)

        header.pack()
        prices.pack()
        different.pack()
        topic.pack()
        end.pack()

    def raise_frame(self):
        self.tkraise()


class friend(tk.Frame):
    def __init__(self, parent, root, controller):
        tk.Frame.__init__(self, parent)
        self.root = root
        self.controller = controller
        self.hotkeys = []

        header = tk.Label(self, text="Friend", font=TITLE_FONT)
        family = tk.Button(self, text="Family", font=BUTTON_FONT)
        job = tk.Button(self, text="Job", font=BUTTON_FONT)
        skills = tk.Button(self, text="Skills", font=BUTTON_FONT)
        different = tk.Button(self, text="Switch Friends", font=BUTTON_FONT)
        topic = tk.Button(self, text="Change Topic", font=BUTTON_FONT)
        end = tk.Button(self, text="End Conversation", font=BUTTON_FONT)

        header.pack()
        family.pack()
        job.pack()
        skills.pack()
        different.pack()
        topic.pack()
        end.pack()

    def raise_frame(self):
        self.tkraise()


gui = tk.Tk()
convo = friend(gui, None, None)
convo.pack()
gui.mainloop()
