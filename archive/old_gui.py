import database as d
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk

import copy

#WARNING: throws error if run from here. Import to economy directory and run from there. Necessary because image files are stored there.

TITLE_FONT = ("Black chancery", "18", "bold")
TEXT_FONT = ("Black chancery", "15")
BUTTON_FONT = ("Black chancery", "13")

class gui(tk.Tk):

    def __init__(self, char, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #char is character controller from ai
        self.char = char
        self.display_cont = None
        self.text_cont = None

        self.hotkeys = []
        self.dynamic_hotkeys = []

        self.wm_title("Jonestown")
        # root.resizable(0,0)

        #megaFrames
        leftSide    =tk.Frame(self)
        rightSide   =tk.Frame(self)

        #frames
        titleImage      = tk.PhotoImage(file="./images/jonestown.gif")
        titleBar        = tk.Label(leftSide, image=titleImage, width=1114, height=150)
        titleBar.image  = titleImage

        display     = display_controller(leftSide,  self)
        printout    = text_output(       leftSide,  self, height=300, width=1114)
        charDisplay = static_data(       rightSide, self, height=474, width=300, background="yellow")
        keyboard    = key_controller(    rightSide, self, height=474, width=300, background="orange")
        self.keyboard = keyboard
        quitter     = quitBar(           rightSide, self,             width=300, background="red")

        #set controllers
        self.display_cont = display
        self.text_cont = printout

        #printout
        printout.grid_propagate(False)

        #charData
        charDisplay.pack_propagate(False)

        #root grid
        leftSide.grid( row=0, column=0, sticky=tk.NSEW)
        rightSide.grid(row=0, column=1, sticky=tk.NSEW)

        #leftSide grid
        titleBar.grid(row=0, column=0)
        display.grid( row=1, column=0)
        printout.grid(row=2, column=0, sticky='nsew')

        #rightSide grid
        charDisplay.grid(row=0, column=0, sticky='nsew')
        keyboard.grid(   row=1, column=0, sticky="nsew")
        rightSide.grid_rowconfigure(1, weight=1)
        rightSide.grid_rowconfigure(0, weight=1)
        quitter.grid(    row=3, column=0, sticky="nsew")

    def getChar(self):
        return self.char

    def addChar(self, char):
        self.char = char

    def get_display_cont(self):
        return self.display_cont

    def get_text_cont(self):
        return self.text_cont

    def out(self, text):
        self.text_cont.out(text)




#display
class display_controller(tk.Frame):

    def __init__(self, parent, root, *args, **kwargs):
        from tutorials import tutorials
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid()

        self.frames = {}

        for display in (matplotlib_display, list_display):
            page_name = display.__name__
            frame = display(parent=self, controller=self, root=root)
            self.frames[page_name] = frame

            #stack frames
            frame.grid(row=0, column=0, sticky="nsew")

        i = 0
        for page_name in ("main_display", "other_display"):
            frame = tutorial(parent=self, controller=self, root=root, text=tutorials[i])
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            i += 1

        self.show_frame("main_display")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.raise_frame()

    def update_frame(self, page_name, *args):
        frame = self.frames[page_name]
        frame.update_frame(*args)
        self.show_frame(page_name)

    def bar_chart(self, x, y, xlabel, ylabel, title):
        self.frames["matplotlib_display"].bar_chart(x, y, xlabel, ylabel, title)
        self.show_frame("matplotlib_display")

    def display_lists(self, col1, col2=None, col3=None, col4=None):
        lists = [col1, col2, col3, col4]
        columns = []

        for array in lists:
            string = ""

            for item in array:
                string += "\n" + str(item)





class tutorial(tk.Frame):

    def __init__(self, parent, controller, root, text):
        tk.Frame.__init__(self, parent)
        self.root = root

        leftBarImage = tk.PhotoImage( file="./images/greenWheat.gif")
        rightBarImage = tk.PhotoImage(file="./images/nightWheat.gif")
        parchment = tk.PhotoImage(    file='./images/parchment.gif')

        leftBar = tk.Label(self, image=leftBarImage, width= 150, height=510)
        leftBar.image = leftBarImage

        self.mainScreen_var = tk.StringVar()
        # intro = """Welcome to Jonestown!

        # You have just inherited a small bakery from your beloved Uncle Bill.
        # Before he died you vowed to him that you would keep his business going.
        
        # He left the bakery well provisioned for the next few days, but you're
        # going to need to build a farm and a mill immediately if you plan on staying in
        # business. 

        # Don't let Uncle Bill down!
        # """

        self.mainScreen_var.set(text)
        mainScreen = tk.Label(self, image=parchment, textvar=self.mainScreen_var,font=TEXT_FONT, width=800, height=500, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)
        mainScreen.image = parchment

        rightBar = tk.Label(self, image=rightBarImage, width=150, height=510)
        rightBar.image = rightBarImage

        leftBar.pack(side=tk.LEFT)
        mainScreen.pack(side=tk.LEFT, expand=True)
        rightBar.pack(side=tk.LEFT)

    def raise_frame(self):
        self.tkraise()

    # def employees(self, unitEmpDict):
    #     text = "Staff"
    #     for unit in unitEmpDict.keys():
    #         text += "\n\n" + unit.name + " employees:"
    #         for employee in unitEmpDict[unit]:
    #             if unitEmpDict[unit].index(employee) % 3 == 0:
    #                 text += "\n"
    #             text += employee.name + " (" + employee.job.jobType +") "
                

    #     self.mainScreen_var.set(text)




class matplotlib_display(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.root = root

        leftBarImage = tk.PhotoImage(file="./images/greenWheat.gif")
        rightBarImage = tk.PhotoImage(file="./images/nightWheat.gif")

        leftBar = tk.Label(self, image=leftBarImage, width= 150, height=510)
        leftBar.image = leftBarImage

        self.fig = Figure(figsize=(6,5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.show()
        graphScreen = self.canvas.get_tk_widget()

        rightBar = tk.Label(self, image=rightBarImage, width=150, height=510)
        rightBar.image = rightBarImage

        leftBar.pack(side=tk.LEFT)
        graphScreen.pack(side=tk.LEFT, expand=True)
        rightBar.pack(side=tk.LEFT)

    # x, y are arrays
    def bar_chart(self, x, y, xlabel, ylabel, title):

        self.fig.clf()
        graph = self.fig.add_subplot(1,1,1)
        x_fill = [i for i in range(len(x))]
        graph.bar(x_fill,y)

        graph.set_title(title)
        graph.set_xlabel(xlabel)
        graph.set_ylabel(ylabel)

        graph.set_xticks(range(len(x)))
        graph.set_xticklabels(x)

    def raise_frame(self):
        self.canvas.show()
        self.tkraise()




class list_display(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.root = root 
        leftBarImage = tk.PhotoImage( file="./images/greenWheat.gif")
        rightBarImage = tk.PhotoImage(file="./images/nightWheat.gif")
        parchment = tk.PhotoImage(    file='./images/parchment.gif')

        leftBar = tk.Label(self, image=leftBarImage, width= 150, height=500)
        leftBar.image = leftBarImage

        self.col1_var = tk.StringVar()
        self.col2_var = tk.StringVar()
        self.col3_var = tk.StringVar()
        self.col4_var = tk.StringVar()

        title1 = tk.Label(self, image=parchment, text="Test",font=TITLE_FONT, width=190, height=30, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)
        title2 = tk.Label(self, image=parchment, text="Test",font=TITLE_FONT, width=190, height=30, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)
        title3 = tk.Label(self, image=parchment, text="Test",font=TITLE_FONT, width=190, height=30, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)
        title4 = tk.Label(self, image=parchment, text="Test",font=TITLE_FONT, width=190, height=30, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)

        col1 = tk.Label(self, image=parchment, textvar=self.col1_var,font=TEXT_FONT, width=190, height=450, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)
        col2 = tk.Label(self, image=parchment, textvar=self.col2_var,font=TEXT_FONT, width=190, height=450, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)
        col3 = tk.Label(self, image=parchment, textvar=self.col3_var,font=TEXT_FONT, width=190, height=450, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)
        col4 = tk.Label(self, image=parchment, textvar=self.col4_var,font=TEXT_FONT, width=190, height=450, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)

        col1.image = parchment

        rightBar = tk.Label(self, image=rightBarImage, width=150, height=500)
        rightBar.image = rightBarImage

        leftBar.grid(row=0, column=0, rowspan=2)

        title1.grid(row=0, column=1)
        title2.grid(row=0, column=2)
        title3.grid(row=0, column=3)
        title4.grid(row=0, column=4)

        col1.grid(row=1, column=1)
        col2.grid(row=1, column=2)
        col3.grid(row=1, column=3)
        col4.grid(row=1, column=4)

        rightBar.grid(row=0, column=5, rowspan=2)

    def raise_frame(self):
        self.tkraise()
        self.display_lists(["hello", "world", "I", "see", "you"], [1,2,3,43,4], ["So", "here", "we", "are"])

    def display_lists(self, col1, col2=None, col3=None, col4=None):
        lists = [col1, col2, col3, col4]
        titles = []
        columns = [self.col1_var, self.col2_var, self.col3_var, self.col4_var]

        for i in range(len(lists)):
            if lists[i] is not None:
                
                string = ""

                for item in lists[i]:

                    string += "\n" + str(item)

                columns[i].set(string)








#printout
class text_output(tk.Frame):

    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root

        self.text = tk.Text(self, background="gray", state='normal', font=TEXT_FONT, width=159, height=20)

        self.text.grid(row=0, column=0, sticky='nsew')
        self.out("Welcome to Jonestown!")

    def out(self, text):
        self.text.insert(tk.INSERT, text)

    def clear(self):
        self.text.delete(1.0, tk.END)








#static_data
class static_data(tk.Frame):

    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root
        
        self.charName = tk.StringVar()
        self.age = tk.StringVar()
        self.locality = tk.StringVar()
        # self.marriage = tk.StringVar()
        self.netWorth = tk.IntVar()

        header =        tk.Label(self, text='Jonestown',                       font=TITLE_FONT)
        nameLabel =     tk.Label(self, textvariable=self.charName, anchor='w', font=TEXT_FONT)
        ageLabel =      tk.Label(self, textvariable=self.age,      anchor='w', font=TEXT_FONT)
        localityLabel = tk.Label(self, textvariable=self.locality, anchor='w', font=TEXT_FONT)
        # marriageLabel = tk.Label(self, textvariable=self.marriage)
        netWorthLabel = tk.Label(self, textvariable=self.netWorth, anchor='w', font=TEXT_FONT)

        self.root.bind("<<refresh>>", self.update_frame)
        self.update_frame()
        self.set_hotkeys()

        header.pack(fill=tk.X)
        nameLabel.pack(fill=tk.X)
        ageLabel.pack(fill=tk.X)
        localityLabel.pack(fill=tk.X)
        # marriageLabel.pack(fill=tk.X)
        netWorthLabel.pack(fill=tk.X)


    def update_frame(self, event=None):
        char = self.root.getChar()
        self.charName.set(char.getName())
        self.age.set("You are " + str(char.getAge()) + " years old.")
        self.locality.set("You live in the town of " + char.getLocality().getName() + ".")
        #should account for property
        self.netWorth.set("Net worth: $" + str(char.getCapital()))

    def set_hotkeys(self):
        
        pass









#controller for which keyboard
class key_controller(tk.Frame):

    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root

        self.root.event_generate("<<refresh>>", when="tail")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid()

        self.frames = {}

        for keyboard in (main_keyboard, 
            new_business, businessData, 
            new_unit, unitData, 
            new_job, jobData, 
            ordersMenu, new_order, 
            market, new_transfer,
            house, town):

            page_name = keyboard.__name__
            frame = keyboard(parent=self, controller=self, root=root)
            self.frames[page_name] = frame

            #stack frames
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("main_keyboard")

    def show_frame(self, page_name, *args):
        frame = self.frames[page_name]
        frame.raise_frame(*args)

    def get_display_cont(self):
        return self.root.get_display_cont()

    def get_text_cont(self):
        return self.root.get_text_cont()

    def get_business(self):
        return self.frames["businessData"].business

    def get_unit(self):
        return self.frames["unitData"].unit

    def get_job(self):
        return self.frames["jobData"].job

    def isInt(self, P):
        isInt = False
        
        try:
            int('0' + P)
            isInt = True
        except ValueError:
            isInt = False

        return isInt

    def create_order(self, order_var, amount_var):
        def callback():
            import orders as o

            business = self.get_business()
            job = self.get_job()
            materialIndex = d.getMaterials().index(order_var.get())

            order = business.craftOrderManager(job, materialIndex)
            order.setAmount(int(amount_var.get()))
            self.root.event_generate("<<refresh>>", when="tail")

        return callback

    def set_order_amount(self, order, amountVar):

        def callback():
            order.setAmount(int(amountVar.get()))
        
        return callback

    def create_transfer(self, order_var, amount_var):
        def callback():
            import orders as o

            business = self.get_business()
            manager = self.get_unit().getJobList()[0]
            materialIndex = d.getMaterials().index(order_var.get())

            transfer = business.transferOrderManager(manager, self.get_unit(), materialIndex)
            transfer.setAmount(int(amount_var.get()))
            self.root.event_generate("<<refresh>>", when="tail")

        return callback

    def show_production(self, entity):
        display_cont = self.root.get_display_cont()
        xy = entity.getProduction()
        products = [d.getMaterials()[xy[0][i]] for i in range(len(xy[0]))]
        display_cont.bar_chart(products, xy[1], "Products", "Crafted", entity.name + " Production")

    def show_employees(self, entity):
        display_cont = self.root.get_display_cont()
        empDict = entity.get_emp_dict()
        x = []
        y = []
        for key in list(empDict.keys()):
            x.append(key.name)
            y.append(len(empDict[key]))

        display_cont.bar_chart(x, y, "Employment", "Employees", entity.name + " Staff")

    def show_stock(self, entity):
        display_cont = self.root.get_display_cont()
        x = d.getMaterials()
        y = entity.getAllStock()
        display_cont.bar_chart(x, y, "Materials", "Amount", entity.name +" Stock")




class main_keyboard(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["h", "t", "n"]
        self.dynamic_buttons = []
        header = tk.Label(self, text="Office", font=TITLE_FONT)
        house = tk.Button(self,   text="h. House",          font=BUTTON_FONT, command=lambda: controller.show_frame("house"))
        town = tk.Button(self,    text="t. Town",           font=BUTTON_FONT, command=lambda: controller.show_frame("town"))
        new_bus = tk.Button(self, text="n. New Business",   font=BUTTON_FONT, command=lambda: controller.show_frame("new_business"))

        header.pack(fill=tk.X)
        house.pack(fill=tk.X)
        town.pack(fill=tk.X)
        new_bus.pack(fill=tk.X)

    def callback_factory(self, business):
        
        def callback(event=None):
            self.controller.show_frame("businessData", business)

        return callback

    def raise_frame(self):
        for button in self.dynamic_buttons:
            button.destroy()

        char = self.root.getChar()
        businesses = char.getBusinesses()

        key = 1
        for business in businesses:
            busi_name = business.getName()

            callback = self.callback_factory(business)
            newButton = tk.Button(self, text= str(callback) + ". " + busi_name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)

        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)

        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("h", lambda x: self.controller.show_frame("house"))
        self.root.bind("t", lambda x: self.controller.show_frame("town"))
        self.root.bind("n", lambda x: self.controller.show_frame("new_business"))

        key = 1
        for button in self.dynamic_buttons:
            self.root.bind(str(key), button.callback)
            self.root.dynamic_hotkeys.append(str(key))
            key += 1




class new_business(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Return>", "<Escape>"]

        header = tk.Label(self, text="Create a New Business", font=TITLE_FONT)
        
        enter_name = tk.Label(self, text="Enter name:", font=TEXT_FONT)
        self.business_name = tk.StringVar()
        self.name = tk.Entry(self, textvariable=self.business_name)

        cash = tk.Label(self, text="Starting cash:", font=TEXT_FONT)

        self.amountVar = tk.StringVar()
        vcmd = (self.register(self.controller.isInt), '%P')
        amount = tk.Entry(self, validatecommand=vcmd, validate="key", textvariable=self.amountVar)
        

        ok = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.create_business)

        esc = tk.Button(self, text="[esc] Return to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        enter_name.pack()
        self.name.pack()
        cash.pack()
        amount.pack()
        ok.pack()
        esc.pack(fill=tk.X)

    def raise_frame(self):
        self.set_hotkeys()
        self.tkraise()
        self.name.focus()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("<Return>", lambda event: self.create_business())
        self.root.bind("<Escape>", lambda event: self.controller.show_frame("main_keyboard"))

    def create_business(self):
        busiName = self.business_name.get()
        busiCash = int("0" + self.amountVar.get())

        new_bus = self.root.char.startBusiness(busiName, busiCash)
        if new_bus is not None:
            self.root.out("\n" + busiName + " created!")
        else:
            self.root.out("\nYou don't have enough money..")

        self.business_name.set("Done!")
        self.root.event_generate("<<refresh>>", when="tail")





class businessData(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        self.hotkeys = ["u", "p", "e", "n", "<Escape>"]
        self.business = None
        self.busiName = tk.StringVar()
        self.busiName.set("nothing")

        header = tk.Label(self, textvariable=self.busiName, font=TITLE_FONT)
        production = tk.Button(self, text="[p] Production", font=BUTTON_FONT, command=lambda: controller.show_production(self.business))
        employees = tk.Button(self, text="[e] Employees", font=BUTTON_FONT, command=lambda: controller.show_employees(self.business))
        new_unit = tk.Button(self, text="[n] New Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("new_unit", business))
        
        callback = lambda event: self.controller.show_frame("main_keyboard")
        self.esc = tk.Button(self, text="[esc] Return to Office", font=BUTTON_FONT, command=callback)
        self.esc.callback = callback

        header.pack(fill=tk.X)
        production.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        new_unit.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def setBusiness(self, business):
        self.business = business
        self.busiName.set(business.getName())

    def raise_frame(self, business):
        for button in self.dynamic_buttons:
            button.destroy()

        self.setBusiness(business)
        char = self.root.getChar()        
        units = business.getUnits()

        key = 1
        for unit in units:
            unit_name = unit.getName()

            callback = lambda event: self.controller.show_frame("unitData", business, unit)
            newButton = tk.Button(self, text=str(key) + ". " + unit_name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        self.esc.pack_forget()
        self.esc.pack(fill=tk.X)

        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("u", lambda event: self.controller.show_frame("unitMenu"))
        self.root.bind("p", lambda event: self.controller.show_production(self.business))
        self.root.bind("e", lambda event: self.controller.show_employees(self.business))
        self.root.bind("n", lambda event: self.controller.show_frame("new_unit", self.business))
        self.root.bind("<Escape>", lambda event: self.controller.show_frame("main_keyboard"))

        key = 1
        for button in self.dynamic_buttons:
            self.root.bind(str(key), button.callback)
            self.root.dynamic_hotkeys.append(str(key))
            key += 1




class new_unit(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        self.hotkeys = ["<Return>", "<Escape>"]
        self.business = None

        header = tk.Label(self, text="New Unit", font=TITLE_FONT)

        unit_label = tk.Label(self, text="Choose a Unit type:", font=TEXT_FONT)
        self.unit_var = tk.StringVar()
        self.unit_name = tk.StringVar()
        unit_list = self.get_units()
        units = tk.OptionMenu(self, self.unit_var, *unit_list)
        name_label = tk.Label(self, text="Name your new Unit:", font=TEXT_FONT)
        self.name = tk.Entry(self, textvariable=self.unit_name)

        ok = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.create_unit)

        callback = lambda event: self.controller.show_frame("businessData", business)
        self.esc = tk.Button(self, text="[esc] Return to Business", font=BUTTON_FONT, command=callback)
        self.esc.callback = callback

        header.pack()
        unit_label.pack()
        units.pack()
        name_label.pack()
        self.name.pack()
        ok.pack()
        self.esc.pack()

    def raise_frame(self, business):
        self.esc.destroy()

        callback = lambda event: self.controller.show_frame("businessData", business)
        self.esc = tk.Button(self, text="[esc] Return to Business", font=BUTTON_FONT, command=callback)
        self.esc.callback = callback
        
        self.esc.pack(fill=tk.X)

        self.set_hotkeys()
        self.tkraise()
        self.name.focus()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.name.bind("<Return>", lambda x: self.create_unit())
        self.root.bind("<Escape>", self.esc.callback)

    def get_units(self):
        from unit import all_units

        unit_list = []

        for unit in all_units():
            unit_list.append(unit.unitType)

        return unit_list

    def create_unit(self):
        from unit import all_units

        unitType = self.unit_var.get()

        for unit in all_units():
            if unit.unitType == unitType:
                break

        name = self.unit_name.get()
        business = self.controller.get_business()
        locality = business.locality
        location = locality.find_property()

        new_unit = unit(name, locality, location, business)
        self.unit_name.set(new_unit)
        self.root.event_generate("<<refresh>>", when="tail")





class unitData(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        self.hotkeys = ["p", "e", "m", "<Escape>"]
        self.business = None
        self.unit = None
        self.unitName = tk.StringVar()
        self.unitName.set("nothing")

        header = tk.Label(self, textvariable=self.unitName, font=TITLE_FONT)
        production = tk.Button(self, text="[p] Production", font=BUTTON_FONT, command=lambda: controller.show_production(self.unit))
        employees = tk.Button(self, text="[e] Employees", font=BUTTON_FONT, command=lambda: controller.show_employees(self.unit))
        market = tk.Button(self, text="[m] Market", font=BUTTON_FONT, command=lambda: controller.show_frame("market", self.business, self.unit))
        new_job = tk.Button(self, text="[n] New job", font=BUTTON_FONT, command=lambda: controller.show_frame("new_job", self.business, self.unit))
        
        callback = lambda event: self.controller.show_frame("businessData", self.business)
        self.esc = tk.Button(self, text="[esc] Return to Business", font=BUTTON_FONT, command=callback)
        self.esc.callback = callback

        header.pack(fill=tk.X)
        production.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        market.pack(fill=tk.X)
        new_job.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def setUnit(self, unit):
        self.unit = unit
        self.unitName.set(unit.getName())

    def raise_frame(self, business, unit):
        for button in self.dynamic_buttons:
            button.destroy()

        self.esc.destroy()

        self.business = business
        self.setUnit(unit)
        char = self.root.getChar()
        jobs = unit.getJobList()

        key = 1
        for job in jobs:
            job_name = job.jobType
            callback = lambda event: self.controller.show_frame("jobData", business, unit, job)
            newButton = tk.Button(self, text=str(key) + ". " + job_name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        callback = lambda event: self.controller.show_frame("businessData", business)
        self.esc = tk.Button(self, text="[esc] Return to Business", font=BUTTON_FONT, command=callback)
        self.esc.callback = callback

        self.esc.pack(fill=tk.X)

        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        # self.root.bind("j", lambda x: self.controller.show_frame("jobsMenu"))
        self.root.bind("p", lambda event: self.controller.show_production(self.unit))
        self.root.bind("e", lambda event: self.controller.show_employees(self.unit))
        self.root.bind("m", lambda event: self.controller.show_frame("market"))
        self.root.bind("n", lambda event: self.controller.show_frame("new_job"))
        self.root.bind("<Escape>", self.esc.callback)

        key = 1
        for button in self.dynamic_buttons:
            self.root.bind(str(key), button.callback)
            self.root.dynamic_hotkeys.append(str(key))
            key += 1




# class jobsMenu(tk.Frame):

#     def __init__(self, parent, controller, root):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         self.root = root
#         self.hotkeys = ["n", "<BackSpace>", "<Escape>"]
#         self.dynamic_buttons = []

#         header = tk.Label(self, text="Jobs", font=TITLE_FONT)
#         new_job = tk.Button(self, text="n. New job", font=BUTTON_FONT, command=lambda: controller.show_frame("new_job"))

#         self.back = tk.Button(self, text="bsp. Back", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData"))
#         self.main = tk.Button(self, text="esc. Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

#         header.pack()
#         new_job.pack(fill=tk.X)
#         self.main.pack(fill=tk.X)

#     def callbackFactory(self, job):
#         def callback(event=None):
#             return self.controller.show_frame("jobData", job)
#         return callback

#     def raise_frame(self):
#         for button in self.dynamic_buttons:
#             button.destroy()

#         char = self.root.getChar()
#         unit = self.controller.get_unit()
#         jobs = unit.getJobList()

#         key = 1
#         for job in jobs:
#             job_name = job.jobType
#             callback = self.callbackFactory(job)
#             newButton = tk.Button(self, text=str(key) + ". " + job_name, font=BUTTON_FONT, command=callback)
#             newButton.callback = callback
#             newButton.pack(fill=tk.X)
#             self.dynamic_buttons.append(newButton)
#             key += 1

#         self.back.pack_forget()
#         self.main.pack_forget()
#         self.back.pack(fill=tk.X)
#         self.main.pack(fill=tk.X)

#         self.set_hotkeys()
#         self.tkraise()

#     def set_hotkeys(self):
#         for hotkey in self.root.hotkeys:
#             self.root.unbind(hotkey)
            
#         for hotkey in self.root.dynamic_hotkeys:
#             self.root.unbind(hotkey)
        
#         self.root.dynamic_hotkeys = []

#         self.root.hotkeys = self.hotkeys
#         self.root.bind("n", lambda x: self.controller.show_frame("new_job"))
#         self.root.bind("<BackSpace>", lambda x: self.controller.show_frame("unitData"))
#         self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))

#         key = 1
#         for button in self.dynamic_buttons:
#             self.root.bind(str(key), button.callback)
#             self.root.dynamic_hotkeys.append(str(key))
#             key += 1



class new_job(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Return>", "<Escape>"]

        header = tk.Label(self, text="New Job", font=TITLE_FONT)

        self.job_var = tk.StringVar()
        job_list = self.get_jobs()
        jobs = tk.OptionMenu(self, self.job_var, *job_list)

        ok = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.create_job)

        # back = tk.Button(self, text="Back", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData"))
        self.esc = tk.Button(self, text="[esc] Return to Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData", unit))

        header.pack()
        jobs.pack()
        ok.pack()
        # back.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def raise_frame(self, business, unit):
        self.esc.destroy()

        callback = lambda event: self.controller.show_frame("unitData", unit)
        self.esc = tk.Button(self, text="[esc] Return to Unit", font=BUTTON_FONT, command=callback)
        self.esc.callback = callback
        
        self.esc.pack(fill=tk.X)

        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("<Return>", lambda event: self.create_job())
        self.root.bind("<Escape>", self.esc.callback)

    def get_jobs(self):
        from jobs import all_jobs
        
        job_list = []

        for job in all_jobs():
            job_list.append(job.jobType)

        return job_list

    def create_job(self):
        from jobs import all_jobs

        jobType = self.job_var.get()

        for job in all_jobs():
            if job.jobType == jobType:
                break

        new_job = job(10, self.controller.get_business(), self.controller.get_unit(), 40)
        self.root.event_generate("<<refresh>>", when="tail")






class jobData(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["o", "e", "<BackSpace>", "<Escape>"]
        self.job = None
        self.jobName = tk.StringVar()
        self.jobName.set("nothing")

        header = tk.Label(self, textvariable=self.jobName,          font=TITLE_FONT)
        orders = tk.Button(self,        text="(o) Orders",          font=BUTTON_FONT, command=lambda: controller.show_frame("ordersMenu"))
        production = tk.Button(self,    text="Production",          font=BUTTON_FONT)
        employees = tk.Button(self,     text="(e) Employees"  ,     font=BUTTON_FONT, command=lambda: controller.show_employees(self.job))
        ledger = tk.Button(self,        text="Ledger",              font=BUTTON_FONT)
        back = tk.Button(self,          text="(bsp) Other jobs",    font=BUTTON_FONT, command=lambda: controller.show_frame("jobsMenu"))
        units = tk.Button(self,         text="(esc) Other units",   font=BUTTON_FONT, command=lambda: controller.show_frame("unitMenu") )

        header.pack(fill=tk.X)
        orders.pack(fill=tk.X)
        production.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        ledger.pack(fill=tk.X)
        back.pack(fill=tk.X)

    def setJob(self, job):
        self.job = job
        self.jobName.set(job.jobType)
    
    def raise_frame(self, job=None):
        if job is not None:
            self.setJob(job)
        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("o", lambda x: self.controller.show_frame("ordersMenu"))
        # self.root.bind("p", lambda x: self.controller.show_production(self.unit))
        self.root.bind("e", lambda x: self.controller.show_employees(self.job))
        self.root.bind("<BackSpace>", lambda x: self.controller.show_frame("jobsMenu"))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("unitMenu"))




class ordersMenu(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["n", "<BackSpace>", "<Escape>"]
        self.dynamic_entries = []
        header = tk.Label(self, text="Orders", font=TITLE_FONT)
        new_order = tk.Button(self, text="n. New order", font=BUTTON_FONT, command=lambda: controller.show_frame("new_order"))
        
        self.back = tk.Button(self, text="bsp. Back", font=BUTTON_FONT, command=lambda: controller.show_frame("jobData"))
        self.main = tk.Button(self, text="esc. Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        new_order.pack(fill=tk.X)
        self.main.pack()

    def cull_wrong_orders(self, orders):
        culled_orders = []

        for order in orders:
            if order.getJob() == self.controller.get_job():
                culled_orders.append(order)

        return culled_orders

    def raise_frame(self):
        for entry in self.dynamic_entries:
            entry.destroy()

        char = self.root.getChar()
        job = self.controller.get_job()
        raw_orders = job.getBusiness().getCraftOrders()
        orders = self.cull_wrong_orders(raw_orders)

        for order in orders:
            newFrame = tk.Frame(self)
            newCaption = tk.Label(newFrame, font=BUTTON_FONT, text=d.getMaterials()[order.getProductIndex()] + ":")
            
            amountVar = tk.StringVar()
            amountVar.set(order.getAmount())
            vcmd = (self.register(self.controller.isInt), '%P')
            newEntry = tk.Entry(newFrame, validatecommand=vcmd, validate="key", textvariable=amountVar)
            newButton = tk.Button(newFrame, font=BUTTON_FONT, text="Ok", command=self.controller.set_order_amount(order, amountVar))

            newCaption.pack(side=tk.LEFT)
            newEntry.pack(side=tk.LEFT)
            newButton.pack(side=tk.LEFT)
            newFrame.pack()
            self.dynamic_entries.append(newFrame)

        self.back.pack_forget()
        self.main.pack_forget()
        self.back.pack(fill=tk.X)
        self.main.pack(fill=tk.X)

        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("n", lambda x: self.controller.show_frame("new_order"))
        self.root.bind("<BackSpace>", lambda x: self.controller.show_frame("jobData"))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))




class new_order(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Return>", "<Escape>"]
        header = tk.Label(self, text="Create a new Order", font=TITLE_FONT)

        products = copy.copy(d.getMaterials())
        self.order_var = tk.StringVar()
        order = tk.OptionMenu(self, self.order_var, *products)

        self.amount_var = tk.StringVar()
        vcmd = (self.register(self.controller.isInt), '%P')
        amount = tk.Entry(self, validatecommand=vcmd, validate="key", textvariable=self.amount_var)

        ok = tk.Button(self, text="OK", font=BUTTON_FONT, command=self.controller.create_order(self.order_var, self.amount_var))
        back = tk.Button(self, text="Back", font=BUTTON_FONT, command=lambda: controller.show_frame("ordersMenu"))
        main = tk.Button(self, text="esc. Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        order.pack()
        amount.pack()
        ok.pack()
        back.pack()
        main.pack()

    def raise_frame(self):
        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        #I don't know why this works
        self.root.bind("<Return>", lambda x: self.controller.create_order(self.order_var, self.amount_var)())
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))




class market(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["n", "<Escape>"]
        self.dynamic_entries = []
        header = tk.Label(self, text="Market", font=TITLE_FONT)
        new_order = tk.Button(self, text="n. New sales line", font=BUTTON_FONT, command=lambda: controller.show_frame("new_transfer"))
        self.back = tk.Button(self, text="Back", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData"))
        self.main = tk.Button(self, text="esc. Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        new_order.pack(fill=tk.X)
        self.back.pack(fill=tk.X)
        self.main.pack(fill=tk.X)

    def raise_frame(self):
        for entry in self.dynamic_entries:
            entry.destroy()

        char = self.root.getChar()
        self.manager = self.controller.get_unit().getJobList()[0]
        raw_orders = self.manager.getBusiness().getTransferOrders()
        orders = self.cull_wrong_orders(raw_orders)

        for order in orders:
            newFrame = tk.Frame(self)
            newCaption = tk.Label(newFrame, font=BUTTON_FONT, text=d.getMaterials()[order.getProductIndex()] + ":")
            
            amountVar = tk.StringVar()
            amountVar.set(order.getAmount())
            vcmd = (self.register(self.controller.isInt), '%P')
            newEntry = tk.Entry(newFrame, validatecommand=vcmd, validate="key", textvariable=amountVar)
            newButton = tk.Button(newFrame, font=BUTTON_FONT, text="Ok", command=self.controller.set_order_amount(order, amountVar))

            newCaption.pack(side=tk.LEFT)
            newEntry.pack(side=tk.LEFT)
            newButton.pack(side=tk.LEFT)
            newFrame.pack()
            self.dynamic_entries.append(newFrame)

        self.back.pack_forget()
        self.main.pack_forget()
        self.back.pack(fill=tk.X)
        self.main.pack(fill=tk.X)

        self.set_hotkeys()
        self.tkraise()

    def cull_wrong_orders(self, orders):
        culled_orders = []

        for order in orders:
            if order.getJob() == self.manager:
                culled_orders.append(order)

        return culled_orders

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []
        self.root.hotkeys = self.hotkeys
        self.root.bind("n", lambda x: self.controller.show_frame("new_transfer"))
        # self.root.bind("<BackSpace>", lambda x: self.controller.show_frame("unitData"))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))




class new_transfer(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Return>", "<Escape>"]
        header = tk.Label(self, text="New Product Line", font=TITLE_FONT)

        products = copy.copy(d.getMaterials())
        self.order_var = tk.StringVar()
        order = tk.OptionMenu(self, self.order_var, *products)

        self.amount_var = tk.StringVar()
        vcmd = (self.register(self.controller.isInt), '%P')
        amount = tk.Entry(self, validatecommand=vcmd, validate="key", textvariable=self.amount_var)

        ok = tk.Button(self, text="OK", font=BUTTON_FONT, command=self.controller.create_transfer(self.order_var, self.amount_var))
        back = tk.Button(self, text="Back", font=BUTTON_FONT, command=lambda: controller.show_frame("market"))
        main = tk.Button(self, text="esc. Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        order.pack()
        amount.pack()
        ok.pack()
        back.pack()
        main.pack()

    def raise_frame(self):
        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        #I don't know why this works
        self.root.bind("<Return>", lambda x: self.controller.create_order(self.order_var, self.amount_var)())
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))




class house(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>"]
        header = tk.Label(self, text="Home",           font=TITLE_FONT)
        main = tk.Button(self,  text="(esc) Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        main.pack(fill=tk.X)

    def raise_frame(self):
        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []
        self.root.hotkeys = self.hotkeys
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))




class town(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>"]
        header = tk.Label(self, text="Town",           font=TITLE_FONT)
        main = tk.Button(self,  text="(esc) Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        main.pack(fill=tk.X)

    def raise_frame(self):
        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []
        self.root.hotkeys = self.hotkeys
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))






class quitBar(tk.Frame):

    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = root

        exit = tk.Button(self,      text="Quit",     font=BUTTON_FONT, command=self.quit)
        next_turn = tk.Button(self, text="[F1] Next day", font=BUTTON_FONT, command=self.next_day)
        self.root.bind("<F1>", self.next_day)
        next_turn.pack(fill=tk.X)
        exit.pack(fill=tk.X)

    def next_day(self, event=None):
        char = self.root.getChar()
        self.root.text_cont.clear()
        char.run_day()

    def quit(self):
        self.root.quit()