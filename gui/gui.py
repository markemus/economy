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
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid()

        self.frames = {}

        for display in (main_display, matplotlib_display):
            page_name = display.__name__
            frame = display(parent=self, controller=self, root=root)
            self.frames[page_name] = frame

            #stack frames
            frame.grid(row=0, column=0, sticky="nsew")

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
        self.mainScreen_var.set("Welcome to Jonestown!")
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

        self.update_frame()

        header.pack(fill=tk.X)
        nameLabel.pack(fill=tk.X)
        ageLabel.pack(fill=tk.X)
        localityLabel.pack(fill=tk.X)
        # marriageLabel.pack(fill=tk.X)
        netWorthLabel.pack(fill=tk.X)


    def update_frame(self):
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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid()

        self.frames = {}

        for keyboard in (main_keyboard, businessMenu, businessData, unitMenu, unitData, jobsMenu, new_job, jobData, 
            ordersMenu, new_order, house, town):
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
            int(P)
            isInt = True
        except ValueError:
            isInt = False

        return isInt

    # def cull_wrong_orders(self, orders):
    #     culled_orders = []

    #     for order in orders:
    #         if order.getJob() == self.get_job():
    #             culled_orders.append(order)

    #     return culled_orders

    def create_order(self, order_var, amount_var):
        def callback():
            import orders as o

            business = self.get_business()
            job = self.get_job()
            materialIndex = d.getMaterials().index(order_var.get())

            order = business.craftOrderManager(job, materialIndex)
            order.setAmount(amount_var.get())

        return callback

    def set_order_amount(self, order, amountVar):

        def callback():
            order.setAmount(int(amountVar.get()))
        
        return callback

    def show_production(self, entity):
        display_cont = self.root.get_display_cont()
        xy = entity.getProduction()
        products = [d.getMaterials()[xy[0][i]] for i in range(len(xy[0]))]
        display_cont.bar_chart(products, xy[1], "Products", "Crafted", "Production")

    def show_employees(self, entity):
        display_cont = self.root.get_display_cont()
        empDict = entity.get_emp_dict()
        x = []
        y = []
        for key in list(empDict.keys()):
            x.append(key.name)
            y.append(len(empDict[key]))

        display_cont.bar_chart(x, y, "Employment", "Employees", entity.name + " Staff")




class main_keyboard(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        header = tk.Label(self,      text="Office",     font=TITLE_FONT)
        businesses = tk.Button(self, text="Businesses", font=BUTTON_FONT, command=lambda: controller.show_frame("businessMenu"))
        house = tk.Button(self,      text="House",      font=BUTTON_FONT, command=lambda: controller.show_frame("house"))
        town = tk.Button(self,       text="Town",       font=BUTTON_FONT, command=lambda: controller.show_frame("town"))

        header.pack(fill=tk.X)
        businesses.pack(fill=tk.X)
        house.pack(fill=tk.X)
        town.pack(fill=tk.X)

    def raise_frame(self):
        self.tkraise()




class businessMenu(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        header = tk.Label(self,     text="Businesses",     font=TITLE_FONT)
        self.main = tk.Button(self, text="Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        self.main.pack(fill=tk.X)

    #we need a separate scope for the business variable of each button- otherwise it will just pass the last one to all.
    def callbackFactory(self, business):
        def callback():
            return self.controller.show_frame("businessData", business)
        return callback

    def raise_frame(self):
        for button in self.dynamic_buttons:
            button.destroy()

        char = self.root.getChar()
        businesses = char.getBusinesses()

        for business in businesses:
            busi_name = business.getName()
            newButton = tk.Button(self, text=busi_name, font=BUTTON_FONT, command=self.callbackFactory(business))
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)

        self.main.pack_forget()
        self.main.pack(fill=tk.X)

        self.tkraise()




class businessData(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.business = None
        self.busiName = tk.StringVar()
        self.busiName.set("nothing")

        header = tk.Label(self, textvariable=self.busiName,       font=TITLE_FONT)
        units = tk.Button(self,         text="Units",             font=BUTTON_FONT, command=lambda: controller.show_frame("unitMenu"))
        production = tk.Button(self,    text="Production",        font=BUTTON_FONT, command=lambda: controller.show_production(self.business))
        employees = tk.Button(self,     text="Employees"  ,       font=BUTTON_FONT, command=lambda: controller.show_employees(self.business))
        ledger = tk.Button(self,        text="Ledger",            font=BUTTON_FONT)
        back = tk.Button(self,          text="Other businesses",  font=BUTTON_FONT, command=lambda: controller.show_frame("businessMenu"))

        header.pack(fill=tk.X)
        units.pack(fill=tk.X)
        production.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        ledger.pack(fill=tk.X)
        back.pack(fill=tk.X)

    def setBusiness(self, business):
        self.business = business
        self.busiName.set(business.getName())

    def raise_frame(self, business):
        self.setBusiness(business)
        self.tkraise()




class unitMenu(tk.Frame):
    
    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        header = tk.Label(self, text="Units", font=TITLE_FONT)

        self.main = tk.Button(self, text="Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        self.main.pack(fill=tk.X)

    def callbackFactory(self, unit):
        def callback():
            return self.controller.show_frame("unitData", unit)
        return callback

    def raise_frame(self):
        for button in self.dynamic_buttons:
            button.destroy()

        char = self.root.getChar()
        business = self.controller.get_business()
        units = business.getUnits()

        for unit in units:
            unit_name = unit.getName()
            newButton = tk.Button(self, text=unit_name, font=BUTTON_FONT, command=self.callbackFactory(unit))
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)

        self.main.pack_forget()
        self.main.pack(fill=tk.X)

        self.tkraise()




class unitData(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.unit = None
        self.unitName = tk.StringVar()
        self.unitName.set("nothing")

        header = tk.Label(self, textvariable=self.unitName,       font=TITLE_FONT)
        jobs = tk.Button(self,          text="Jobs",               font=BUTTON_FONT, command=lambda: controller.show_frame("jobsMenu"))
        production = tk.Button(self,    text="Production",        font=BUTTON_FONT, command=lambda: controller.show_production(self.unit))
        employees = tk.Button(self,     text="Employees"  ,       font=BUTTON_FONT, command=lambda: controller.show_employees(self.unit))
        ledger = tk.Button(self,        text="Ledger",            font=BUTTON_FONT)
        back = tk.Button(self,          text="Other units",       font=BUTTON_FONT, command=lambda: controller.show_frame("unitMenu"))

        header.pack(fill=tk.X)
        jobs.pack(fill=tk.X)
        production.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        ledger.pack(fill=tk.X)
        back.pack(fill=tk.X)

    def setUnit(self, unit):
        self.unit = unit
        self.unitName.set(unit.getName())

    def raise_frame(self, unit):
        self.setUnit(unit)
        self.tkraise()




class jobsMenu(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        header = tk.Label(self, text="Jobs", font=TITLE_FONT)
        new_job = tk.Button(self, text="New job", font=BUTTON_FONT, command=lambda: controller.show_frame("new_job"))
        self.main = tk.Button(self, text="Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        new_job.pack(fill=tk.X)
        self.main.pack(fill=tk.X)

    def callbackFactory(self, job):
        def callback():
            return self.controller.show_frame("jobData", job)
        return callback

    def raise_frame(self):
        for button in self.dynamic_buttons:
            button.destroy()

        char = self.root.getChar()
        unit = self.controller.get_unit()
        jobs = unit.getJobList()

        for job in jobs:
            job_name = job.jobType
            newButton = tk.Button(self, text=job_name, font=BUTTON_FONT, command=self.callbackFactory(job))
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)

        self.main.pack_forget()
        self.main.pack(fill=tk.X)

        self.tkraise()




class new_job(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root

        header = tk.Label(self, text="New Job", font=TITLE_FONT)

        self.job_var = tk.StringVar()
        job_list = self.get_jobs()
        jobs = tk.OptionMenu(self, self.job_var, *job_list)

        ok = tk.Button(self, text="Ok", font=BUTTON_FONT, command=self.create_job)
        main = tk.Button(self, text="Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        jobs.pack()
        ok.pack()
        main.pack(fill=tk.X)

    def raise_frame(self):
        self.tkraise()

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






class jobData(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.job = None
        self.jobName = tk.StringVar()
        self.jobName.set("nothing")

        header = tk.Label(self, textvariable=self.jobName,        font=TITLE_FONT)
        orders = tk.Button(self,        text="Orders",            font=BUTTON_FONT, command=lambda: controller.show_frame("ordersMenu"))
        production = tk.Button(self,    text="Production",        font=BUTTON_FONT)
        employees = tk.Button(self,     text="Employees"  ,       font=BUTTON_FONT, command=lambda: controller.show_employees(self.job))
        ledger = tk.Button(self,        text="Ledger",            font=BUTTON_FONT)
        back = tk.Button(self,          text="Other jobs",        font=BUTTON_FONT, command=lambda: controller.show_frame("jobsMenu"))
        units = tk.Button(self,         text="Other units",       font=BUTTON_FONT, command=lambda: controller.show_frame("unitMenu") )

        header.pack(fill=tk.X)
        orders.pack(fill=tk.X)
        production.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        ledger.pack(fill=tk.X)
        back.pack(fill=tk.X)

    def setJob(self, job):
        self.job = job
        self.jobName.set(job.jobType)
    
    def raise_frame(self, job):
        self.setJob(job)
        self.tkraise()




class ordersMenu(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_entries = []
        header = tk.Label(self, text="Orders", font=TITLE_FONT)
        new_order = tk.Button(self, text="New order", font=BUTTON_FONT, command=lambda: controller.show_frame("new_order"))
        self.main = tk.Button(self, text="Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))


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

        self.main.pack_forget()
        self.main.pack(fill=tk.X)

        self.tkraise()




class new_order(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        header = tk.Label(self, text="Create a new Order", font=TITLE_FONT)

        products = copy.copy(d.getMaterials())
        order_var = tk.StringVar()
        order = tk.OptionMenu(self, order_var, *products)

        amount_var = tk.StringVar()
        vcmd = (self.register(self.controller.isInt), '%P')
        amount = tk.Entry(self, validatecommand=vcmd, validate="key", textvariable=amount_var)

        ok = tk.Button(self, text="OK", font=BUTTON_FONT, command=self.controller.create_order(order_var, amount_var))
        main = tk.Button(self, text="Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack()
        order.pack()
        amount.pack()
        ok.pack()
        main.pack()

    def raise_frame(self):
        self.tkraise()

    # def isInt(self, P):
    #     isInt = False
        
    #     try:
    #         int(P)
    #         isInt = True
    #     except ValueError:
    #         isInt = False

    #     return isInt

    # def set_amount(self, order, amountVar):

    #     def callback():
    #         order.setAmount(int(amountVar.get()))
        
    #     return callback

    # def create_order(self):
    #     import orders as o

    #     business = self.controller.get_business()
    #     job = self.controller.get_job()
    #     materialIndex = d.getMaterials().index(self.order_var.get())

    #     order = business.craftOrderManager(job, materialIndex)
    #     order.setAmount(self.amount_var.get())




class house(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        header = tk.Label(self, text="Home",           font=TITLE_FONT)
        main = tk.Button(self,  text="Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        main.pack(fill=tk.X)

    def raise_frame(self):
        self.tkraise()




class town(tk.Frame):

    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        header = tk.Label(self, text="Town",           font=TITLE_FONT)
        main = tk.Button(self,  text="Back to office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        main.pack(fill=tk.X)

    def raise_frame(self):
        self.tkraise()








class quitBar(tk.Frame):

    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = root

        exit = tk.Button(self,      text="Quit",     font=BUTTON_FONT, command=self.quit)
        next_turn = tk.Button(self, text="Next day", font=BUTTON_FONT, command=self.next_day)
        next_turn.pack(fill=tk.X)
        exit.pack(fill=tk.X)

    def next_day(self):
        char = self.root.getChar()
        self.root.text_cont.clear()
        char.run_day()

    def quit(self):
        self.root.quit()