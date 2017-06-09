import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk

import copy

import database as d
import tutorials

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

        self.display_cont   = display_controller(   leftSide,  self)
        self.text_cont      = text_output(          leftSide,  self, height=300, width=1114)
        charDisplay         = static_data(          rightSide, self, height=474, width=300, background="yellow")
        keyboard            = key_controller(       rightSide, self, height=474, width=300, background="orange")
        quitter             = quitBar(              rightSide, self,             width=300, background="red")        

        #printout
        self.text_cont.grid_propagate(False)

        #charData
        self.display_cont.pack_propagate(False)

        #root grid
        leftSide.grid( row=0, column=0, sticky=tk.NSEW)
        rightSide.grid(row=0, column=1, sticky=tk.NSEW)

        #leftSide grid
        titleBar.grid(row=0, column=0)
        self.display_cont.grid( row=1, column=0)
        self.text_cont.grid(row=2, column=0, sticky='nsew')

        #rightSide grid
        charDisplay.grid(row=0, column=0, sticky='nsew')
        keyboard.grid(   row=1, column=0, sticky="nsew")
        rightSide.grid_rowconfigure(1, weight=1)
        rightSide.grid_rowconfigure(0, weight=1)
        quitter.grid(    row=3, column=0, sticky="nsew")

        self.display_cont.show_frame("list_display")

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
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid()

        self.frames = {}

        for display in (main_display, matplotlib_display, list_display):
            page_name = display.__name__
            frame = display(parent=self, controller=self, root=root)
            self.frames[page_name] = frame

            #stack frames
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("list_display")

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

    def display_list(self, values_dict):
        self.frames["list_display"].display_list(values_dict)
        self.show_frame("list_display")





class main_display(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.root = root

        leftBarImage = tk.PhotoImage( file="./images/greenWheat.gif")
        rightBarImage = tk.PhotoImage(file="./images/nightWheat.gif")
        parchment = tk.PhotoImage(    file='./images/parchment.gif')

        leftBar = tk.Label(self, image=leftBarImage, width= 150, height=510)
        leftBar.image = leftBarImage

        self.mainScreen_var = tk.StringVar()
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

    def update_frame(self, text=None):
        self.mainScreen_var.set(text)

    def employees(self, unitEmpDict):
        text = "Staff"
        for unit in unitEmpDict.keys():
            text += "\n\n" + unit.name + " employees:"
            for employee in unitEmpDict[unit]:
                if unitEmpDict[unit].index(employee) % 3 == 0:
                    text += "\n"
                text += employee.name + " (" + employee.job.jobType +") "
                

        self.mainScreen_var.set(text)




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

        self.display_var = tk.StringVar()

        self.display = tk.Label(self, image=parchment, textvar=self.display_var,font=TEXT_FONT, width=800, height=500, borderwidth=5, 
            relief=tk.RIDGE, compound=tk.CENTER)

        self.display.image = parchment

        rightBar = tk.Label(self, image=rightBarImage, width=150, height=500)
        rightBar.image = rightBarImage

        leftBar.grid(row=0, column=0)
        self.display.grid(row=0, column=1)
        rightBar.grid(row=0, column=2)

    def raise_frame(self):
        self.tkraise()

    def display_list(self, values_dict):
        string = "List \n\n"
        for key in values_dict.keys():
            string += "\n" + str(key) + ": " + str(values_dict[key])

        self.display_var.set(string)








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

        for keyboard in (
            welcome, main_keyboard, 
            # new_business, 
            businessData, 
            new_unit, unitData, ledger,
            new_job, jobData, 
            new_order, 
            market, new_transfer, new_transport,
            house, people_profiles, store_profiles,
            town):

            page_name = keyboard.__name__
            frame = keyboard(parent=self, controller=self, root=root)
            self.frames[page_name] = frame

            #stack frames
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("welcome")

    def show_frame(self, page_name, *args):
        frame = self.frames[page_name]
        self.root.focus()
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
            amount = int("0" + amount_var.get())
            order.setAmount(amount)
            self.root.event_generate("<<refresh>>", when="tail")

        return callback

    def set_order_amount(self, order, amountVar):

        def callback():
            amount = int("0" + amountVar.get())
            order.setAmount(amount)
        
        return callback

    def create_transfer(self, order_var, amount_var):
        def callback():
            import orders as o

            business = self.get_business()
            manager = self.get_unit().staff.manager
            materialIndex = d.getMaterials().index(order_var.get())

            transfer = business.transferOrderManager(manager, self.get_unit(), materialIndex)
            amount = int("0" + amount_var.get())
            transfer.setAmount(amount)
            self.root.event_generate("<<refresh>>", when="tail")

        return callback

    def create_transport(self, endunit, order_var, amount_var):
        import orders as o

        business = self.get_business()
        carrier = self.get_unit().staff.carrier
        materialIndex = d.getMaterials().index(order_var.get())

        transport = business.transportOrderManager(carrier, self.get_unit(), endunit, materialIndex)
        amount = int("0" + amount_var.get())
        transport.setAmount(amount)
        self.root.event_generate("<<refresh>>", when="tail")

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

    def show_p_profile(self, profile):
        display_cont = self.root.get_display_cont()
        values_dict = profile.get_values()
        display_cont.show_profile(values_dict)




class welcome(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Return>"]

        header = tk.Label(self, text="Welcome", font=TITLE_FONT)
        self.name_var = tk.StringVar()
        name_label = tk.Label(self, text="Name:", font=TEXT_FONT)
        self.name = tk.Entry(self, textvariable=self.name_var)
        enter = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.set_name)

        header.pack()
        name_label.pack()
        self.name.pack()
        enter.pack()

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.welcome)

    def raise_frame(self):
        self.set_hotkeys()
        self.show_splash()
        self.tkraise()
        self.name.focus()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)

        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)

        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("<Return>", self.set_name)

    def set_name(self, event=None):
        name = self.name_var.get()
        self.root.char.setName(name)
        self.root.event_generate("<<refresh>>", when="tail")
        self.controller.show_frame("main_keyboard")

class main_keyboard(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        self.hotkeys = ["h", "t"] # "n"
        header = tk.Label(self,      text="Office",     font=TITLE_FONT)
        house = tk.Button(self,      text="[h] House",      font=BUTTON_FONT, command=lambda: controller.show_frame("house"))
        town = tk.Button(self,       text="[t] Town",       font=BUTTON_FONT, command=lambda: controller.show_frame("town"))
        # new_bus = tk.Button(self,    text="[n] New Business", font=BUTTON_FONT, command=lambda: controller.show_frame("new_business"))

        header.pack(fill=tk.X)
        house.pack(fill=tk.X)
        town.pack(fill=tk.X)
        # new_bus.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.main_display)

    #we need a separate scope for the business variable of each button- otherwise it will just pass the last one to all.
    def callbackFactory(self, business):
        def callback(event=None):
            return self.controller.show_frame("businessData", business)
        return callback

    def raise_frame(self):
        for button in self.dynamic_buttons:
            button.destroy()

        self.dynamic_buttons = []

        char = self.root.getChar()
        businesses = char.getBusinesses()

        key =1
        for business in businesses:
            busi_name = business.getName()
            callback = self.callbackFactory(business)
            newButton = tk.Button(self, text= "[" + str(key) + "] " + busi_name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        self.set_hotkeys()
        self.show_splash()
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
        # self.root.bind("n", lambda x: self.controller.show_frame("new_business"))

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

        header = tk.Label(self, text="Create a new Business", font=TITLE_FONT)
        name_label = tk.Label(self, text="Business name:", font=TEXT_FONT)

        self.business_name = tk.StringVar()
        self.name = tk.Entry(self, textvariable=self.business_name)

        cash = tk.Label(self, text="Starting cash:", font=TEXT_FONT)

        self.amountVar = tk.StringVar()
        vcmd = (self.register(self.controller.isInt), '%P')
        amount = tk.Entry(self, validatecommand=vcmd, validate="key", textvariable=self.amountVar)
        enter = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.create_business)
        esc = tk.Button(self, text="[esc] Return to Office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        name_label.pack()
        self.name.pack()
        cash.pack()
        amount.pack()
        enter.pack()
        esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.new_business)

    def raise_frame(self):
        self.set_hotkeys()
        self.show_splash()
        self.tkraise()
        self.name.focus()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("<Return>", lambda x: self.create_business())
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))

    def create_business(self):
        busiName = self.business_name.get()
        busiCash = int("0" + self.amountVar.get())

        new_bus = self.root.char.startBusiness(busiName, busiCash)
        if new_bus is not None:
            self.root.out("\n" + busiName + " created!")
        else:
            self.root.out("\nYou don't have enough money.")

        self.business_name.set("Done!")
        self.root.event_generate("<<refresh>>", when="tail")





class businessData(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        self.hotkeys = ["s", "p", "e", "n", "<Escape>"]
        self.business = None
        self.busiName = tk.StringVar()
        self.busiName.set("busiName")

        header = tk.Label(self, textvariable=self.busiName,     font=TITLE_FONT)
        stock = tk.Button(self, text= "[s] Stock", font = BUTTON_FONT, command=lambda: controller.show_stock(self.business))
        production = tk.Button(self, text="[p] Production", font=BUTTON_FONT, command=lambda: controller.show_production(self.business))
        employees = tk.Button(self, text="[e] Employees", font=BUTTON_FONT, command=lambda: controller.show_employees(self.business))
        new_unit = tk.Button(self,text="[n] New Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("new_unit"))
        self.esc = tk.Button(self,text="[esc] Return to Office",font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        stock.pack(fill=tk.X)
        production.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        new_unit.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def setBusiness(self, business):
        self.business = business
        self.busiName.set(business.getName())

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.businessData)

    def callbackFactory(self, unit):
        def callback(event=None):
            return self.controller.show_frame("unitData", unit)
        return callback

    def raise_frame(self, business=None):
        if business is not None:
            self.setBusiness(business)
        business = self.business

        for button in self.dynamic_buttons:
            button.destroy()
        self.dynamic_buttons = []

        char = self.root.getChar()
        units = business.getUnits()

        key = 1
        for unit in units:
            unit_name = unit.getName()
            callback = self.callbackFactory(unit)
            newButton = tk.Button(self, text="[" + str(key) + "] " + unit_name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        self.esc.pack_forget()
        self.esc.pack(fill=tk.X)
        
        self.set_hotkeys()
        self.show_splash()
        # self.controller.show_stock(self.business)
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("s", lambda x: self.controller.show_stock(self.business))
        self.root.bind("p", lambda x: self.controller.show_production(self.business))
        self.root.bind("e", lambda x: self.controller.show_employees(self.business))
        self.root.bind("n", lambda x: self.controller.show_frame("new_unit"))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))

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
        self.hotkeys = ["<Return>", "<Escape>"]

        header = tk.Label(self, text="Create a new Unit", font=TITLE_FONT)

        self.unit_var = tk.StringVar()
        self.unit_name = tk.StringVar()
        unit_list = self.get_units()
        units = tk.OptionMenu(self, self.unit_var, *unit_list)
        self.name = tk.Entry(self, textvariable=self.unit_name)

        enter = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.create_unit)
        esc = tk.Button(self, text="[esc] Return to Business", font=BUTTON_FONT, command=lambda: controller.show_frame("businessData"))

        header.pack()
        units.pack()
        self.name.pack()
        enter.pack()
        esc.pack(fill=tk.X)
    
    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.new_unit)

    def raise_frame(self):
        self.set_hotkeys()
        self.show_splash()
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
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("businessData"))

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
        self.hotkeys = ["s", "p", "e", "m", "n","<Escape>"]
        self.unit = None
        self.unitName = tk.StringVar()
        self.unitName.set("unitName")

        header = tk.Label(self, textvariable=self.unitName, font=TITLE_FONT)
        stock = tk.Button(self, text="[s] Stock", font=BUTTON_FONT, command=lambda: controller.show_stock(self.unit))
        production = tk.Button(self, text="[p] Production", font=BUTTON_FONT, command=lambda: controller.show_production(self.unit))
        employees = tk.Button(self, text="[e] Employees", font=BUTTON_FONT, command=lambda: controller.show_employees(self.unit))
        market = tk.Button(self, text="[m] Market", font=BUTTON_FONT, command=lambda: controller.show_frame("market"))
        new_job = tk.Button(self, text="[n] New Job", font=BUTTON_FONT, command=lambda: controller.show_frame("new_job"))
        self.esc = tk.Button(self, text="[esc] Return to Business", font=BUTTON_FONT, command=lambda: controller.show_frame("businessData"))

        header.pack(fill=tk.X)
        stock.pack(fill=tk.X)
        production.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        market.pack(fill=tk.X)
        new_job.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def setUnit(self, unit):
        self.unit = unit
        self.unitName.set(unit.getName())

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.unitData)

    def callbackFactory(self, job):
        def callback(event=None):
            return self.controller.show_frame("jobData", job)
        return callback

    def raise_frame(self, unit=None):
        if unit is not None:
            self.setUnit(unit)
        unit = self.unit

        for button in self.dynamic_buttons:
            button.destroy()
        self.dynamic_buttons = []

        char = self.root.getChar()
        unit = self.controller.get_unit()
        jobs = unit.getJobList()

        key = 1
        for job in jobs:
            job_name = job.jobType
            callback = self.callbackFactory(job)
            newButton = tk.Button(self, text="[" + str(key) + "] " + job_name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        self.esc.pack_forget()
        self.esc.pack(fill=tk.X)

        self.set_hotkeys()
        self.show_splash()
        # self.controller.show_stock(self.unit)
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("s", lambda x: self.controller.show_stock(self.unit))
        self.root.bind("p", lambda x: self.controller.show_production(self.unit))
        self.root.bind("e", lambda x: self.controller.show_employees(self.unit))
        self.root.bind("m", lambda x: self.controller.show_frame("market"))
        self.root.bind("n", lambda x: self.controller.show_frame("new_job"))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("businessData"))

        key = 1
        for button in self.dynamic_buttons:
            self.root.bind(str(key), button.callback)
            self.root.dynamic_hotkeys.append(str(key))
            key += 1




class ledger(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["w", "c", "s", "p" "<Escape>"]

        header = tk.Label(self, text="Ledger", font=TITLE_FONT)
        weekly = tk.Button(self, text="[w] Weekly summary", font=BUTTON_FONT)
        crafted = tk.Button(self, text="[c] Crafted over time", font=BUTTON_FONT)
        sales = tk.Button(self, text="[s] Sales over time", font=BUTTON_FONT)
        prices = tk.Button(self, text="[p] Prices over time", font=BUTTON_FONT)

    def raise_frame(self):
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        # self.root.bind("s", lambda x: self.controller.show_stock(self.unit))
        # self.root.bind("p", lambda x: self.controller.show_production(self.unit))
        # self.root.bind("e", lambda x: self.controller.show_employees(self.unit))
        # self.root.bind("m", lambda x: self.controller.show_frame("market"))
        # self.root.bind("n", lambda x: self.controller.show_frame("new_job"))
        # self.root.bind("<Escape>", lambda x: self.controller.show_frame("businessData"))


class new_job(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Return>", "<Escape>"]

        header = tk.Label(self, text="Create a new Job", font=TITLE_FONT)

        self.job_var = tk.StringVar()
        job_list = self.get_jobs()
        jobs = tk.OptionMenu(self, self.job_var, *job_list)

        enter = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.create_job)
        esc = tk.Button(self, text="[esc] Return to Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData"))

        header.pack()
        jobs.pack()
        enter.pack()
        esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.new_job)

    def raise_frame(self):
        self.set_hotkeys()
        self.show_splash()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("<Return>", lambda x: self.create_job())
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("unitData"))

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
        self.dynamic_buttons = []
        self.hotkeys = ["e", "n", "<Escape>"]
        self.job = None
        self.jobName = tk.StringVar()
        self.jobName.set("nothing")

        header = tk.Label(self, textvariable=self.jobName,          font=TITLE_FONT)
        production = tk.Button(self,    text="Production",          font=BUTTON_FONT)
        employees = tk.Button(self,     text="[e] Employees"  ,     font=BUTTON_FONT, command=lambda: controller.show_employees(self.job))
        new_order = tk.Button(self,     text="[n] New Order", font=BUTTON_FONT, command=lambda: controller.show_frame("new_order"))
        self.esc = tk.Button(self,      text="[esc] Return to Unit",font=BUTTON_FONT, command=lambda: controller.show_frame("unitData") )

        header.pack(fill=tk.X)
        production.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        new_order.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def setJob(self, job):
        self.job = job
        self.jobName.set(job.jobType)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.jobData)

    def cull_wrong_orders(self, orders):
        culled_orders = []

        for order in orders:
            if order.getJob() == self.controller.get_job():
                culled_orders.append(order)

        return culled_orders

    def raise_frame(self, job=None):
        if job is not None:
            self.setJob(job)
        job = self.job
        
        for entry in self.dynamic_buttons:
            entry.destroy()
        self.dynamic_buttons = []

        char = self.root.getChar()

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
            self.dynamic_buttons.append(newFrame)

        self.esc.pack_forget()
        self.esc.pack(fill=tk.X)

        self.show_splash()
        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        self.root.bind("e", lambda x: self.controller.show_employees(self.job))
        self.root.bind("n", lambda x: self.controller.show_frame("new_order"))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("unitData"))




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

        enter = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.controller.create_order(self.order_var, self.amount_var))
        esc = tk.Button(self, text="[esc] Return to Job", font=BUTTON_FONT, command=lambda: controller.show_frame("jobData"))

        header.pack()
        order.pack()
        amount.pack()
        enter.pack()
        esc.pack()

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.new_order)

    def raise_frame(self):
        self.set_hotkeys()
        self.show_splash()
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
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("jobData"))




class market(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["n", "t", "<Escape>"]
        self.dynamic_buttons = []
        header = tk.Label(self, text="Market", font=TITLE_FONT)
        new_order = tk.Button(self, text="[n] New sales line", font=BUTTON_FONT, command=lambda: controller.show_frame("new_transfer"))
        new_transport = tk.Button(self, text="[t] New transport line", font=BUTTON_FONT, command=lambda: controller.show_frame("new_transport"))
        self.esc = tk.Button(self, text="[esc] Return to Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData"))

        header.pack()
        new_order.pack(fill=tk.X)
        new_transport.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.market)

    def raise_frame(self):
        for entry in self.dynamic_buttons:
            entry.destroy()

        char = self.root.getChar()
        self.manager = self.controller.get_unit().staff.manager
        self.carrier = self.controller.get_unit().staff.carrier
        raw_transfers = self.manager.getBusiness().getTransferOrders()
        raw_transports = self.manager.getBusiness().getTransportOrders()
        transfers = self.cull_wrong_orders(raw_transfers, self.manager)
        transports = self.cull_wrong_orders(raw_transports, self.carrier)

        orderTitle = tk.Label(self, text="Transfers:", font=TEXT_FONT)
        self.dynamic_buttons.append(orderTitle)
        orderTitle.pack()

        self.spawn_orders(transfers)

        transportTitle = tk.Label(self, text="Transports:", font=TEXT_FONT)
        self.dynamic_buttons.append(transportTitle)
        transportTitle.pack()
        
        self.spawn_orders(transports)

        self.esc.pack_forget()
        self.esc.pack(fill=tk.X)

        self.show_splash()
        self.set_hotkeys()
        self.tkraise()

    def spawn_orders(self, orders):
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
            self.dynamic_buttons.append(newFrame)

    def cull_wrong_orders(self, orders, job):
        culled_orders = []

        for order in orders:
            if order.getJob() == job:
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
        self.root.bind("t", lambda x: self.controller.show_frame("new_transport"))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("unitData"))




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

        enter = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.controller.create_transfer(self.order_var, self.amount_var))
        esc = tk.Button(self, text="[esc] Return to Market", font=BUTTON_FONT, command=lambda: controller.show_frame("market"))

        header.pack()
        order.pack()
        amount.pack()
        enter.pack()
        esc.pack()

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.new_transfer)

    def raise_frame(self):
        self.set_hotkeys()
        self.show_splash()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        #I don't know why this works
        self.root.bind("<Return>", lambda x: self.controller.create_transfer(self.order_var, self.amount_var)())
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("market"))


class new_transport(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        self.hotkeys = ["<Return>", "<Escape>"]
        header = tk.Label(self, text="Transports", font=TITLE_FONT)
        direct = tk.Label(self, text="Transfer Stock to other Units", font=TEXT_FONT)

        order_label = tk.Label(self, text="Transfer:", font=TEXT_FONT)
        products = copy.copy(d.getMaterials())
        self.order_var = tk.StringVar()
        order = tk.OptionMenu(self, self.order_var, *products)

        endunit_label = tk.Label(self, text="Transfer to:", font=TEXT_FONT)
        self.endunit = tk.StringVar()

        self.amount_var = tk.StringVar()
        vcmd = (self.register(self.controller.isInt), '%P')
        self.amount = tk.Entry(self, validatecommand=vcmd, validate="key", textvariable=self.amount_var)

        self.enter = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.create_transport)
        self.esc = tk.Button(self, text="[esc] Return to Market", font=BUTTON_FONT, command=lambda: controller.show_frame("market"))

        header.pack()
        order_label.pack()
        order.pack()
        endunit_label.pack()
        self.amount.pack()
        self.enter.pack()
        self.esc.pack()

    def end_unit(self):
        return self.endunit

    def create_transport(self, event=None):
        # units = copy.copy(self.controller.get_unit().getBusiness().getUnits())
        unitname = self.endunit.get()

        endunit = "failed"

        for unit in self.units:
            if unit.name == unitname:
                endunit = unit
                break

        self.controller.create_transport(endunit, self.order_var, self.amount_var)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.new_transport)

    def raise_frame(self):
        for button in self.dynamic_buttons:
            button.destroy()
        self.dynamic_buttons = []

        self.units = copy.copy(self.controller.get_unit().getBusiness().getUnits())
        
        unitnames = []
        for unit in self.units:
            unitnames.append(unit.name)

        end_unit_list = tk.OptionMenu(self, self.endunit, *unitnames)
        self.dynamic_buttons.append(end_unit_list)
        # self.units = units

        self.amount.pack_forget()
        self.enter.pack_forget()
        self.esc.pack_forget()

        end_unit_list.pack()
        self.amount.pack()
        self.enter.pack()
        self.esc.pack()

        self.set_hotkeys()
        self.show_splash()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []

        self.root.hotkeys = self.hotkeys
        #I don't know why this works
        self.root.bind("<Return>", self.create_transport)
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("market"))








class house(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["s","p","<Escape>"]
        header = tk.Label(self, text="Home", font=TITLE_FONT)
        p_profiles = tk.Button(self, text="[p] People profiles", font=BUTTON_FONT, command=lambda: controller.show_frame("people_profiles"))
        s_profiles = tk.Button(self, text="[s] Store profiles", font=BUTTON_FONT, command=lambda: controller.show_frame("store_profiles"))
        esc = tk.Button(self,  text="[esc] Return to Office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        p_profiles.pack(fill=tk.X)
        s_profiles.pack(fill=tk.X)
        esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.house)

    def raise_frame(self):
        self.set_hotkeys()
        self.show_splash()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []
        self.root.hotkeys = self.hotkeys
        self.root.bind("p", lambda x: self.controller.show_frame("people_profiles"))
        self.root.bind("s", lambda x: self.controller.show_frame("store_profiles"))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))




class people_profiles(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>"]
        self.dynamic_buttons  = []
        header = tk.Label(self, text="People Profiles", font=TITLE_FONT)
        self.esc = tk.Button(self, text="[esc] Return to House", font=BUTTON_FONT, command=lambda: self.controller.show_frame("house"))

        header.pack()
        self.esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.people_profiles)

    def callbackFactory(self, profile):
        def callback(event=None):
            return self.root.display_cont.display_list(profile.get_values())
        return callback
    
    def raise_frame(self):
        for entry in self.dynamic_buttons:
            entry.destroy()

        char = self.root.getChar()
        profiles = char.getKnownPeople()

        key =1
        for profile in profiles:
            # pname = profile.name
            callback = self.callbackFactory(profile)
            newButton = tk.Button(self, text= "[" + str(key) + "] " + profile.name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        self.esc.pack_forget()
        self.esc.pack(fill=tk.X)

        self.show_splash()
        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []
        self.root.hotkeys = self.hotkeys
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("house"))

        key = 1
        for button in self.dynamic_buttons:
            self.root.bind(str(key), button.callback)
            self.root.dynamic_hotkeys.append(str(key))
            key += 1




class store_profiles(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>"]
        self.dynamic_buttons = []
        header = tk.Label(self, text="Store Profiles", font=TITLE_FONT)
        self.esc = tk.Button(self, text="[esc] Return to House", font=BUTTON_FONT, command=lambda:self.controller.show_frame("house"))

        header.pack()
        self.esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.store_profiles)

    def callbackFactory(self, profile):
        def callback(event=None):
            return self.controller.show_frame("s_profile_data", profile)
        return callback
    
    def raise_frame(self):
        for entry in self.dynamic_buttons:
            entry.destroy()

        char = self.root.getChar()
        profiles = char.getKnownStores()

        key =1
        for profile in profiles:
            # pname = profile.name
            callback = self.callbackFactory(profile)
            newButton = tk.Button(self, text= "[" + str(key) + "] " + profile.name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        self.esc.pack_forget()
        self.esc.pack(fill=tk.X)

        self.show_splash()
        self.set_hotkeys()
        self.tkraise()

    def set_hotkeys(self):
        for hotkey in self.root.hotkeys:
            self.root.unbind(hotkey)
            
        for hotkey in self.root.dynamic_hotkeys:
            self.root.unbind(hotkey)
        
        self.root.dynamic_hotkeys = []
        self.root.hotkeys = self.hotkeys
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("house"))

        key = 1
        for button in self.dynamic_buttons:
            self.root.bind(str(key), button.callback)
            self.root.dynamic_hotkeys.append(str(key))
            key += 1








class town(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>"]
        header = tk.Label(self, text="Town",           font=TITLE_FONT)
        main = tk.Button(self,  text="[esc] Return to Office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        main.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.town)

    def raise_frame(self):
        self.set_hotkeys()
        self.show_splash()
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
        next_turn = tk.Button(self, text="[f1] Next Day", font=BUTTON_FONT, command=self.next_day)
        self.root.bind("<F1>", self.next_day)
        next_turn.pack(fill=tk.X)
        exit.pack(fill=tk.X)

    def next_day(self, event=None):
        char = self.root.getChar()
        self.root.text_cont.clear()
        char.run_day()

    def quit(self):
        self.root.quit()