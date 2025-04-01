import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk
import tkinter.scrolledtext as st

import tkinter.font

import copy
from operator import attrgetter

import database as d
import tutorials
# tkscrollframe is a custom package that extends tkframes with a scrollbar. Standard solution from web.
from tkscrollframe import tkscrollframe as tsf

# WARNING: throws error if run from here. Import to economy directory and run from there. Necessary because image files are stored there.
# TITLE_FONT = ("Courier", "18", "bold")
# TEXT_FONT = ("Courier", "15", "bold")
# BUTTON_FONT = ("Courier", "13")

TITLE_FONT = ("Black chancery", "18", "bold")

# TITLE_FONT = tkinter.font.Font(root=None, family='Helvetica', size='18', weight='bold', underline=1)
TEXT_FONT = ("Black chancery", "15")
BUTTON_FONT = ("Black chancery", "13")
MAP_FONT = ("Consolas", "9")


# TODO business aggregate info-
#  EG show all transports and transfers
#  show ledger (same as for unit)
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
        # TODO fix screen sizing issue.
        # TODO currently text gets cut off on the main display when not full sized.
        # self.resizable(0,0)
        self.resizable(1,1)
        # self.geometry('1414x940')
        self.geometry('1366x768')
        # self.geometry('680x240')

        # megaFrames
        leftSide    = tk.Frame(self)
        rightSide   = tk.Frame(self)

        # frames
        titleImage      = tk.PhotoImage(file="./images/jonestown.gif")
        titleBar        = tk.Label(leftSide, image=titleImage, width=1114, height=150)
        titleBar.image  = titleImage

        self.display_cont   = display_controller(   leftSide,  self)
        self.text_cont      = text_output(          leftSide,  self, height=150, width=900)
        # self.text_cont      = text_output(          leftSide,  self, height=150, width=700)
        charDisplay         = static_data(          rightSide, self, height=100, width=300)
        busDisplay          = bus_static_data(      rightSide, self, height=100, width=300)
        keyboard            = key_controller(       rightSide, self, height=474, width=300)
        quitter             = quitBar(              rightSide, self,             width=300)
        self.static_cont   = static_controller(self, charDisplay, busDisplay)

        # printout
        self.text_cont.grid_propagate(False)

        # charData
        self.display_cont.pack_propagate(False)

        # root grid
        leftSide.grid(row=0, column=0, sticky=tk.NSEW)
        rightSide.grid(row=0, column=1, sticky=tk.NSEW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Setting weight=0 makes the buttons be visible on smaller screens. I have no idea why this works.
        self.grid_columnconfigure(1, weight=0)

        # leftSide grid
        titleBar.grid(row=0, column=0)
        self.display_cont.grid(row=1, column=0)
        self.text_cont.grid(row=2, column=0, sticky='nsew')
        leftSide.grid_rowconfigure(0, weight=1)
        leftSide.grid_rowconfigure(1, weight=1)
        leftSide.grid_rowconfigure(2, weight=1)
        leftSide.grid_columnconfigure(0, weight=1)

        # rightSide grid
        charDisplay.grid(row=0, column=0, sticky='nsew')
        busDisplay.grid( row=1, column=0, sticky='nsew')
        keyboard.grid(   row=2, column=0, sticky="nsew")
        rightSide.grid_rowconfigure(0, weight=0)
        rightSide.grid_rowconfigure(1, weight=0)
        rightSide.grid_rowconfigure(2, weight=1)
        quitter.grid(    row=3, column=0, sticky="nsew")

        # self.display_cont.show_frame("main_display")
        # self.display_cont.line_chart([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], [[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]], "hello", "world", "title")

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


#  display
class display_controller(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid()

        self.frames = {}

        for display in (main_display, matplotlib_display, list_display, canvas_display):
            page_name = display.__name__
            frame = display(parent=self, controller=self, root=root)
            self.frames[page_name] = frame

            # stack frames
            frame.grid(row=0, column=0, sticky="nsew")

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

    def line_chart(self, x, y, xlabel, ylabel, title, legend=None):
        self.frames["matplotlib_display"].line_chart(x, y, xlabel, ylabel, title, legend=legend)
        self.show_frame("matplotlib_display")

    def display_list(self, values_dict):
        self.frames["list_display"].display_list(values_dict)
        self.show_frame("list_display")

    def display_spreadsheet(self, spreadsheet):
        self.frames["list_display"].display_spreadsheet(spreadsheet)
        self.show_frame("list_display")

    def display_p_profile(self, values_dict):
        self.frames["canvas_display"].display_p_profile(values_dict)
        self.show_frame("canvas_display")

    def display_s_profile(self, values_dict):
        self.frames["canvas_display"].display_s_profile(values_dict)
        self.show_frame("canvas_display")

    def display_m_profile(self, values_dict):
        self.frames["canvas_display"].display_m_profile(values_dict)
        self.show_frame("canvas_display")

    def display_c_profile(self, values_dict):
        self.frames["canvas_display"].display_c_profile(values_dict)
        self.show_frame("canvas_display")

    def display_map(self, localmap):
        self.frames["canvas_display"].display_map(localmap)
        self.show_frame("canvas_display")


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
        mainScreen = tk.Label(self, image=parchment, textvar=self.mainScreen_var, font=TEXT_FONT, width=800, height=500, borderwidth=5,
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

        self.fig = Figure(figsize=(8,5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        # self.canvas.show()
        self.canvas.draw()
        graphScreen = self.canvas.get_tk_widget()
        graphScreen.config(borderwidth=5, relief=tk.RIDGE)

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
        # graph.grid()

    def line_chart(self, x, y, xlabel, ylabel, title, legend=None):
        """legend = optional list of strings that name the xvals."""
        self.fig.clf()
        graph = self.fig.add_subplot(111)
        
        for z in y:
            graph.plot(x, z, "o-")

        if legend:
            graph.legend(legend)

        graph.set_title(title)
        graph.set_xlabel(xlabel)
        graph.set_ylabel(ylabel)
        graph.grid()

    def raise_frame(self):
        # self.canvas.show()
        self.canvas.draw()
        self.tkraise()


class list_display(tk.Frame):
    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.root = root 
        leftBarImage = tk.PhotoImage( file="./images/greenWheat.gif")
        rightBarImage = tk.PhotoImage(file="./images/nightWheat.gif")
        parchment = tk.PhotoImage(    file='./images/parchment.gif')

        leftBar = tk.Label(self, image=leftBarImage, width= 150, height=510)
        leftBar.image = leftBarImage

        self.display_var = tk.StringVar()
        self.display = tk.Label(self, image=parchment, textvar=self.display_var, font=TEXT_FONT, width=800, height=500, borderwidth=5,
            relief=tk.RIDGE, compound=tk.CENTER, justify=tk.LEFT)
        self.display.image = parchment

        rightBar = tk.Label(self, image=rightBarImage, width=150, height=510)
        rightBar.image = rightBarImage

        leftBar.grid(row=0, column=0)
        self.display.grid(row=0, column=1)
        rightBar.grid(row=0, column=2)

    def raise_frame(self):
        self.tkraise()

    def display_list(self, values_dict):
        string = "List \n"
        for key in sorted(values_dict.keys(), key=str.lower):
            string += "\n" + str(key) + ": " + str(values_dict[key])

        self.display_var.set(string)

    #can handle up to six columns
    def display_spreadsheet(self, spreadsheet):

        def justify(item):
            spaces = " " + (" " * (8 - len(item))) + "|"
            item = item[:8]
            item += spaces
            return item

        string = "Spreadsheet \n"
        for array in spreadsheet:
            string += "\n"
            
            for item in array:
                string += justify(item)

        self.display_var.set(string)


class canvas_display(tk.Frame):
    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.root = root 
        leftBarImage = tk.PhotoImage( file="./images/greenWheat.gif")
        rightBarImage = tk.PhotoImage(file="./images/nightWheat.gif")
        parchment = tk.PhotoImage(    file='./images/parchment.gif')

        leftBar = tk.Label(self, image=leftBarImage, width=150, height=510)
        leftBar.image = leftBarImage

        self.display = tk.Canvas(self, width=800, height=500, borderwidth=5, relief=tk.RIDGE)
        self.display.create_image(6, 6, anchor="nw", image=parchment, tag="background")
        self.display.image = parchment

        self.scroller = tk.Scrollbar(self, orient="vertical", command=self.custom_yview)
        self.display.configure(yscrollcommand=self.scroller.set)

        rightBar = tk.Label(self, image=rightBarImage, width=150, height=510)
        rightBar.image = rightBarImage

        leftBar.grid(row=0, column=0)
        self.display.grid(row=0, column=1)
        self.scroller.grid(row=0, column=2)
        # self.grid_columnconfigure(2, minsize=100)  # Here
        rightBar.grid(row=0, column=3)

    def custom_yview(self, *args, **kwargs):
        self.display.yview(*args, **kwargs)
        x = self.display.canvasx(0)
        y = self.display.canvasy(0)
        self.display.coords("background", x, y)

    def raise_frame(self):
        self.display.yview_moveto(0)
        x = self.display.canvasx(0)
        y = self.display.canvasy(0)
        self.display.coords("background", x, y)
        self.tkraise()

    def display_p_profile(self, values_dict):
        details = (
            "Name: " + values_dict["name"] + "\n" +
            "Opinion: " + values_dict["opinion"] + "\n" +
            "DOB: " + values_dict["birthday"] + "\n" +
            "Met on: " + values_dict["meton"] + "\n"
            "Works as a " + values_dict["job"] + "\n" +
            # "Skills: " + values_dict["skills"] + "\n" +  
            "Lives at " + values_dict["house"] + " in " + values_dict["locality"] + "\n" +
            "Married to " + values_dict["spouse"] + "\n" +
            "Parents: " + values_dict["father"] + " and " + values_dict["mother"] + "\n" +
            # "Siblings: " + values_dict["siblings"] + "\n" +
            # "Children: " + values_dict["children"] + "\n" +
            "Needs: " + values_dict["mu"] + "\n")

        self.display.delete("temp")
        self.display.create_text(395, 20, text="Person Profile", font=TITLE_FONT, tags="temp")
        self.display.create_rectangle(30, 30, 170, 170, tags="temp")
        self.display.create_text(200, 30, text=details, anchor="nw", font=TEXT_FONT, tags="temp")

    def display_s_profile(self, values_dict):
        details = ("Name: " + values_dict["name"] + "\n" +
            "Prices: " + values_dict["prices"] + "\n" +
            "Familiarity: " + values_dict["familiarity"] + "\n" +
            "Experience: " + values_dict["experience"] + "\n" +
            "Location: " + values_dict["location"] + "\n" +
            "How did you hear about us?: " + values_dict["heardabout"] + "\n")

        self.display.delete("temp")
        self.display.create_text(395, 20, text="Store Profile", font=TITLE_FONT, tags="temp")
        self.display.create_text(10, 30, text=details, anchor="nw", font=TEXT_FONT, tags="temp")

    def display_m_profile(self, values_dict):
        details = ("Name: " + values_dict["name"] + "\n" +
            # "Prices: " + values_dict["prices"] + "\n" +
            "Familiarity: " + values_dict["familiarity"] + "\n" +
            "Experience: " + values_dict["experience"] + "\n" +
            "Location: " + values_dict["location"] + "\n" +
            "How did you hear about us?: " + values_dict["heardabout"] + "\n")

        self.display.delete("temp")
        self.display.create_text(395, 20, text="Factory Profile", font=TITLE_FONT, tags="temp")
        self.display.create_text(10, 30, text=details, anchor="nw", font=TEXT_FONT, tags="temp")

    def display_c_profile(self, values_dict):
        details = ("Name: " + values_dict["name"] + "\n" +
            # "Prices: " + values_dict["prices"] + "\n" +
            "Familiarity: " + values_dict["familiarity"] + "\n" +
            "Experience: " + values_dict["experience"] + "\n" +
            "Location: " + values_dict["location"] + "\n" +
            "How did you hear about us?: " + values_dict["heardabout"] + "\n")

        self.display.delete("temp")
        self.display.create_text(395, 20, text="Church Profile", font=TITLE_FONT, tags="temp")
        self.display.create_text(10, 30, text=details, anchor="nw", font=TEXT_FONT, tags="temp")

    def display_map(self, localmap):
        self.display.delete("temp")
        self.display.create_text(10, 10, text=localmap, anchor="nw", font=MAP_FONT, tags="temp")


# printout
class text_output(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs)
        self.root = root

        self.text = st.ScrolledText(self, background="gray", state='normal', font=TEXT_FONT, width=112, height=10, borderwidth=5, 
            relief=tk.RIDGE,)

        self.text.pack(side="left", fill="both", expand=True)
        self.out("Welcome to Jonestown!\n")

    def out(self, text):
        self.text.insert(tk.INSERT, text)

    def clear(self):
        self.text.delete(1.0, tk.END)


# hacky, but I don't care!
class static_controller(object):
    def __init__(self, root, static_data, bus_static_data):
        self.root = root
        self.static_data = static_data
        self.bus_static_data = bus_static_data

        self.root.bind("<<refresh>>", self.update_statics)

    def update_statics(self, event=None):
        self.static_data.update_frame()
        self.bus_static_data.update_frame()


# static_data
class static_data(tk.Frame):

    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs, borderwidth=5, relief=tk.RIDGE)
        self.root = root
        
        self.charName = tk.StringVar()
        # self.age = tk.StringVar()
        self.locality = tk.StringVar()
        self.marriage = tk.StringVar()
        self.netWorth = tk.StringVar()
        self.happiness = tk.StringVar()

        # header =        tk.Label(self, text='Jonestown',                       font=TITLE_FONT)
        nameLabel =     tk.Label(self, textvariable=self.charName, font=TITLE_FONT)
        # ageLabel =      tk.Label(self, textvariable=self.age,      anchor='w', font=TEXT_FONT)
        localityLabel = tk.Label(self, textvariable=self.locality, anchor='w', font=TEXT_FONT)
        marriageLabel = tk.Label(self, textvariable=self.marriage, anchor='w', font=TEXT_FONT)
        netWorthLabel = tk.Label(self, textvariable=self.netWorth, anchor='w', font=TEXT_FONT)
        happinessLabel= tk.Label(self, textvariable=self.happiness, anchor='w', font=TEXT_FONT)

        # header.pack(fill=tk.X)
        nameLabel.pack(fill=tk.X)
        marriageLabel.pack(fill=tk.X)
        localityLabel.pack(fill=tk.X)
        # ageLabel.pack(fill=tk.X)       
        netWorthLabel.pack(fill=tk.X)
        happinessLabel.pack(fill=tk.X)

    def update_frame(self, event=None):
        char = self.root.getChar()
        self.charName.set(char.name)
        # self.age.set(str(char.getAge()) + " years old.")
        self.locality.set("Lives in the town of " + char.getLocality().getName() + ".")
        self.marriage.set("Married to " + str(char.spouse.name) + ".")
        #should account for property
        self.netWorth.set("Cash: $" + str(round(char.getCapital(), 2)))
        self.happiness.set("Satisfaction: " + str(char.getHappiness()))


class bus_static_data(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, master=parent, *args, **kwargs, borderwidth=5, relief=tk.RIDGE)
        self.root = root

        self.bus_name = tk.StringVar()
        self.bus_cash = tk.StringVar()
        self.units = tk.StringVar()
        self.employees = tk.StringVar()

        nameLabel = tk.Label(self, textvariable=self.bus_name, anchor="w", font=TITLE_FONT)
        cashLabel = tk.Label(self, textvariable=self.bus_cash, anchor="w", font=TEXT_FONT)
        unitsLabel = tk.Label(self, textvariable=self.units, anchor="w", font=TEXT_FONT)
        employeesLabel = tk.Label(self, textvariable=self.employees, anchor="w", font=TEXT_FONT)

        nameLabel.pack(fill=tk.X)
        cashLabel.pack(fill=tk.X)
        unitsLabel.pack(fill=tk.X)
        employeesLabel.pack(fill=tk.X)

    def update_frame(self, event=None):
        bus = self.root.getChar().getBusinesses()[0]
        self.bus_name.set(bus.name)
        self.bus_cash.set("Capital: $" + str(round(bus.getCash(), 2)))
        self.units.set("Units: " + str(len(bus.getUnits())))
        self.employees.set("Employees: " + str(len(bus.getEmployees())))


# controller for which keyboard
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
            house, 
            people_profiles, 
            store_profiles,
            manu_profiles,
            church_profiles,
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

    # TODO create transfer and transport orders manually as well.
    def create_order(self, order_var, amount_var):
        def callback():
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
            # manager = self.get_unit().staff.manager
            materialIndex = d.getMaterials().index(order_var.get())

            transfer = business.transferOrderManager(self.get_unit(), materialIndex)
            amount = int("0" + amount_var.get())
            transfer.setAmount(amount)
            self.root.event_generate("<<refresh>>", when="tail")

        return callback

    def create_transport(self, endunit, order_var, amount_var):
        import orders as o

        business = self.get_business()
        # carrier = self.get_unit().staff.carrier
        materialIndex = d.getMaterials().index(order_var.get())

        transport = business.transportOrderManager(self.get_unit(), endunit, materialIndex)
        amount = int("0" + amount_var.get())
        transport.setAmount(amount)
        self.root.event_generate("<<refresh>>", when="tail")

    def show_production(self, entity):
        display_cont = self.root.get_display_cont()
        xy = entity.getProduction()
        products = [d.getMaterials()[xy[0][i]] for i in range(len(xy[0]))]
        display_cont.bar_chart(products, xy[1], "Products", "Crafted", entity.name + " Production")

    def show_sales(self, entity):
        display_cont = self.root.get_display_cont()
        xy = entity.getSales()
        products = [d.getMaterials()[xy[0][i]] for i in range(len(xy[0]))]
        display_cont.bar_chart(products, xy[1], "Products", "Sold", entity.name + " Sales")

    def show_prices(self, entity):
        display_cont = self.root.get_display_cont()
        x = d.getMaterials()
        y = entity.getPrice()
        display_cont.bar_chart(x, y, "Products", "Prices", entity.name + " Prices")

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
        display_cont.bar_chart(x, y, "Materials", "Amount", entity.name + " Stock")

    def show_ledger(self, unit, i, which):
        display_cont = self.root.get_display_cont()
        ledger_legend = ["Price", "Direct Material Cost", "Crafted", "Sales", "Failed Sales", "Transports", "Failed Transports", "Stock", "Output"]
        dayCount = unit.getDayNum() + 1
        if dayCount >= 30:
            dayCount = 30
        x = list(range(1, dayCount))
        fakey = unit.bigdata.getMonth(i)
        y = []
        legend = []

        for j in range(len(which)):
            if which[j] == 1:
                y.append(fakey[j])
                legend.append(ledger_legend[j])

        # display_cont.line_chart(x, y, d.getMaterials()[i], "Amount", unit.name + " " + d.getMaterials()[i], legend)
        display_cont.line_chart(x, y, "Days", "Amount", unit.name + " " + d.getMaterials()[i], legend)

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
        if len(name) != 0:
            self.root.char.name = name
        self.root.event_generate("<<refresh>>", when="tail")
        self.controller.show_frame("main_keyboard")




# class main_keyboard(tk.Frame):
class main_keyboard(tsf.tkscrollframe):

    def __init__(self, parent, controller, root):
        # tk.Frame.__init__(self, parent)
        tsf.tkscrollframe.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        self.hotkeys = ["h", "t"] # "n"
        header = tk.Label(self.frame,      text="Office",     font=TITLE_FONT)
        house = tk.Button(self.frame,      text="[h] House",      font=BUTTON_FONT, command=lambda: controller.show_frame("house"))
        town = tk.Button(self.frame,       text="[t] Town",       font=BUTTON_FONT, command=lambda: controller.show_frame("town"))
        # TODO-DECIDE enable multiple businesses? Currently indicated in tutorials that is possible (but is not)
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
            newButton = tk.Button(self.frame, text= "[" + str(key) + "] " + busi_name, font=BUTTON_FONT, command=callback)
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




# class businessData(tk.Frame):
class businessData(tsf.tkscrollframe):

    def __init__(self, parent, controller, root):
        # tk.Frame.__init__(self, parent)
        tsf.tkscrollframe.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        self.hotkeys = ["s", "c", "d", "e", "n", "<Escape>"]
        self.business = None
        self.busiName = tk.StringVar()
        self.busiName.set("busiName")

        header = tk.Label(self.frame, textvariable=self.busiName,     font=TITLE_FONT)
        stock = tk.Button(self.frame, text= "[s] Stock", font = BUTTON_FONT, command=lambda: controller.show_stock(self.business))
        production = tk.Button(self.frame, text="[c] Crafted", font=BUTTON_FONT, command=lambda: controller.show_production(self.business))
        sales = tk.Button(self.frame, text="[d] Demand", font=BUTTON_FONT, command=lambda: controller.show_sales(self.business))
        employees = tk.Button(self.frame, text="[e] Employees", font=BUTTON_FONT, command=lambda: controller.show_employees(self.business))
        # TODO add business prices screen
        # prices = tk.Button(self.frame, text="[p] Prices", font=BUTTON_FONT, command=lambda: controller.show_prices(self.business))
        new_unit = tk.Button(self.frame, text="[n] New Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("new_unit"))
        self.esc = tk.Button(self.frame, text="[esc] Return to Office",font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        stock.pack(fill=tk.X)
        production.pack(fill=tk.X)
        sales.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        # prices.pack(fill=tk.X)
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
            newButton = tk.Button(self.frame, text="[" + str(key) + "] " + unit_name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        self.esc.pack_forget()
        self.esc.pack(fill=tk.X)
        
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
        self.root.bind("s", lambda x: self.controller.show_stock(self.business))
        self.root.bind("c", lambda x: self.controller.show_production(self.business))
        self.root.bind("d", lambda x: self.controller.show_sales(self.business))
        self.root.bind("e", lambda x: self.controller.show_employees(self.business))
        # self.root.bind("p", lambda x: self.controller.show_prices(self.business))
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
        if unit.zoningType == "f":
            location = locality.find_sized_property(zone=unit.zoningType, xsize=5, ysize=5)
        else:
            location = locality.find_property(zone=unit.zoningType)

        if location is not None:
            new_unit = unit(name, locality, location, business)

            if unit.zoningType == "f":
                locality.claim_nodes_from_topleft(location, xsize=5, ysize=5, entity=new_unit)
            else:
                locality.claim_node(location, new_unit)
    
            # TODO should go to unit page instead of this debug display.
            self.unit_name.set(new_unit)
            self.root.event_generate("<<refresh>>", when="tail")


# TODO figure out why buttons are pushed to the left side, except in business frame?
class unitData(tsf.tkscrollframe):
    def __init__(self, parent, controller, root):
        # tk.Frame.__init__(self, parent)
        tsf.tkscrollframe.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.dynamic_buttons = []
        self.hotkeys = ["s", "c", "d", "e", "p", "l", "m", "n","<Escape>"]
        self.unit = None
        self.unitName = tk.StringVar()
        self.unitName.set("unitName")

        header = tk.Label(self.frame, textvariable=self.unitName, font=TITLE_FONT)
        stock = tk.Button(self.frame, text="[s] Stock", font=BUTTON_FONT, command=lambda: controller.show_stock(self.unit))
        production = tk.Button(self.frame, text="[c] Crafted", font=BUTTON_FONT, command=lambda: controller.show_production(self.unit))
        sales = tk.Button(self.frame, text="[d] Demand", font=BUTTON_FONT, command=lambda: controller.show_sales(self.unit))
        employees = tk.Button(self.frame, text="[e] Employees", font=BUTTON_FONT, command=lambda: controller.show_employees(self.unit))
        prices = tk.Button(self.frame, text="[p] Prices", font=BUTTON_FONT, command=lambda: controller.show_prices(self.unit))
        ledger = tk.Button(self.frame, text="[l] Ledger", font=BUTTON_FONT, command=lambda: controller.show_frame("ledger"))
        market = tk.Button(self.frame, text="[m] Market", font=BUTTON_FONT, command=lambda: controller.show_frame("market"))
        new_job = tk.Button(self.frame, text="[n] New Job", font=BUTTON_FONT, command=lambda: controller.show_frame("new_job"))
        self.esc = tk.Button(self.frame, text="[esc] Return to Business", font=BUTTON_FONT, command=lambda: controller.show_frame("businessData"))

        header.pack(fill=tk.X)
        stock.pack(fill=tk.X)
        production.pack(fill=tk.X)
        sales.pack(fill=tk.X)
        employees.pack(fill=tk.X)
        prices.pack(fill=tk.X)
        ledger.pack(fill=tk.X)
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
            newButton = tk.Button(self.frame, text="[" + str(key) + "] " + job_name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            key += 1

        self.esc.pack_forget()
        self.esc.pack(fill=tk.X)

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
        self.root.bind("s", lambda x: self.controller.show_stock(self.unit))
        self.root.bind("c", lambda x: self.controller.show_production(self.unit))
        self.root.bind("d", lambda x: self.controller.show_sales(self.unit))
        self.root.bind("e", lambda x: self.controller.show_employees(self.unit))
        self.root.bind("p", lambda x: self.controller.show_prices(self.unit))
        self.root.bind("l", lambda x: self.controller.show_frame("ledger"))
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
        self.hotkeys = ["<Return>" "<Escape>"]
        self.dynamic_buttons = []

        # main
        header = tk.Label(self, text="Ledger", font=TITLE_FONT)
        self.mat = tk.IntVar()
        self.left = tk.Frame(self)
        self.right = tk.Frame(self)
        enter = tk.Button(self, text="[enter] Go!", font=BUTTON_FONT, command=lambda: controller.show_ledger(self.controller.get_unit(), self.mat.get(), (self.price.get(), self.DMC.get(), self.crafted.get(), self.sales.get(), self.failSales.get(), self.transports.get(), self.failTransports.get(), self.stock.get(), self.output.get())))
        esc = tk.Button(self, text="[esc] Return to Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData"))

        # right
        self.price = tk.IntVar(value=1)
        self.DMC = tk.IntVar(value=1)
        self.crafted = tk.IntVar(value=1)
        self.sales = tk.IntVar(value=1)        
        self.failSales = tk.IntVar(value=1)
        self.transports = tk.IntVar(value=1)
        self.failTransports = tk.IntVar(value=1)
        self.stock = tk.IntVar(value=1)
        self.output = tk.IntVar(value=1)

        p_button = tk.Checkbutton(self.right, text="Price", font=BUTTON_FONT, variable=self.price)
        d_button = tk.Checkbutton(self.right, text="Direct Material Cost", font=BUTTON_FONT, variable=self.DMC)
        c_button = tk.Checkbutton(self.right, text="Crafted", font=BUTTON_FONT, variable=self.crafted)
        s_button = tk.Checkbutton(self.right, text="Sales", font=BUTTON_FONT, variable=self.sales)
        fs_button = tk.Checkbutton(self.right, text="Failed Sales", font=BUTTON_FONT, variable=self.failSales)
        t_button = tk.Checkbutton(self.right, text="Transports", font=BUTTON_FONT, variable=self.transports)
        ft_button = tk.Checkbutton(self.right, text="FailedTransports", font=BUTTON_FONT, variable=self.failTransports)
        stock_button = tk.Checkbutton(self.right, text="Stock", font=BUTTON_FONT, variable=self.stock)
        output_button = tk.Checkbutton(self.right, text="Output", font=BUTTON_FONT, variable=self.output)

        p_button.pack(anchor="w")
        d_button.pack(anchor="w")
        c_button.pack(anchor="w")
        s_button.pack(anchor="w")
        fs_button.pack(anchor="w")
        t_button.pack(anchor="w")
        ft_button.pack(anchor="w")
        stock_button.pack(anchor="w")
        output_button.pack(anchor="w")
        
        header.grid(row=0, column=0, columnspan=2, sticky="new")
        self.left.grid(row=1, column=0, sticky="n")
        self.right.grid(row=1, column=1, sticky="n")
        enter.grid(row=2, column=0, columnspan=2, sticky="new")
        esc.grid(row=3, column=0, columnspan=2, stick="new")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def raise_frame(self):
        
        for button in self.dynamic_buttons:
            button.destroy()

        key = 0
        for material in d.getMaterials():
            button = tk.Radiobutton(self.left, text=material, font=BUTTON_FONT, variable=self.mat, value=key)
            self.dynamic_buttons.append(button)
            button.pack(anchor="w")
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
        self.root.bind("<Return>", lambda x: self.controller.show_ledger(self.controller.get_unit(), self.mat.get(), (self.price.get(), self.DMC.get(), self.crafted.get(), self.sales.get(), self.failSales.get(), self.transports.get(), self.failTransports.get(), self.stock.get(), self.output.get())))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("unitData"))


class new_job(tk.Frame):
    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Return>", "<Escape>"]

        header = tk.Label(self, text="Create a new Job", font=TITLE_FONT)

        self.job_var = tk.StringVar()
        # job_list = self.get_jobs()
        self.jobs = tk.OptionMenu(self, self.job_var, ["empty"])

        enter = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.create_job)
        esc = tk.Button(self, text="[esc] Return to Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData"))

        header.pack()
        self.jobs.pack()
        enter.pack()
        esc.pack(fill=tk.X)

    def update_menu(self, values):
        menu = self.jobs["menu"]
        menu.delete(0, "end")

        # Add new values
        for val in values:
            menu.add_command(label=val, command=lambda v=val: self.job_var.set(v))

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.new_job)

    def raise_frame(self):
        self.set_hotkeys()
        self.update_menu(self.get_jobs())
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
        # from jobs import all_jobs
        #
        # job_list = []
        #
        # for job in all_jobs():
        #     job_list.append(job.jobType)
        unit = self.controller.get_unit()
        if unit:
            jobTypes = [j.jobType for j in unit.allowed_jobs]
        else:
            jobTypes = [""]
        return jobTypes

    def create_job(self):
        jobType = self.job_var.get()

        for job in self.controller.get_unit().allowed_jobs:
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

        header = tk.Label(self, textvariable=self.jobName,           font=TITLE_FONT)
        # production = tk.Button(self,    text="Production",          font=BUTTON_FONT)
        employees = tk.Button(self,     text="[e] Employees",        font=BUTTON_FONT, command=lambda: controller.show_employees(self.job))
        new_order = tk.Button(self,     text="[n] New Order",        font=BUTTON_FONT, command=lambda: controller.show_frame("new_order"))
        self.esc = tk.Button(self,      text="[esc] Return to Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData") )

        header.pack(fill=tk.X)
        # production.pack(fill=tk.X)
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
        self.order = tk.OptionMenu(self, self.order_var, *products)

        self.amount_var = tk.StringVar()
        vcmd = (self.register(self.controller.isInt), '%P')
        amount = tk.Entry(self, validatecommand=vcmd, validate="key", textvariable=self.amount_var)

        enter = tk.Button(self, text="[enter]", font=BUTTON_FONT, command=self.controller.create_order(self.order_var, self.amount_var))
        esc = tk.Button(self, text="[esc] Return to Job", font=BUTTON_FONT, command=lambda: controller.show_frame("jobData"))

        header.pack()
        self.order.pack()
        amount.pack()
        enter.pack()
        esc.pack()

    def update_menu(self, values):
        menu = self.order["menu"]
        menu.delete(0, "end")

        # Add new values
        for val in values:
            menu.add_command(label=val, command=lambda v=val: self.order_var.set(v))

    def get_orderables(self):
        """Returns a list of materials the job is able to create."""
        job = self.controller.get_job()
        orderables = []
        for i, mat in enumerate(d.getMaterials()):
            if job.can_make[i]:
                orderables.append(mat)
        return orderables

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.new_order)

    def raise_frame(self):
        self.update_menu(self.get_orderables())
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
        self.new_order = tk.Button(self, text="[n] New sales line", font=BUTTON_FONT, command=lambda: controller.show_frame("new_transfer"))
        self.new_transport = tk.Button(self, text="[t] New transport line", font=BUTTON_FONT, command=lambda: controller.show_frame("new_transport"))
        self.esc = tk.Button(self, text="[esc] Return to Unit", font=BUTTON_FONT, command=lambda: controller.show_frame("unitData"))

        header.pack()
        self.new_order.pack(fill=tk.X)
        self.new_transport.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.market)

    def raise_frame(self):
        for entry in self.dynamic_buttons:
            entry.destroy()

        self.new_order.pack_forget()
        self.new_transport.pack_forget()

        # vars
        char = self.root.getChar()
        self.manager = self.controller.get_unit().staff.manager
        self.carrier = self.controller.get_unit().staff.carrier
        raw_transfers = self.manager.getBusiness().getTransferOrders()
        raw_transports = self.manager.getBusiness().getTransportOrders()
        transfers = self.cull_wrong_orders(raw_transfers, self.manager)
        transports = self.cull_wrong_orders(raw_transports, self.carrier)

        # sales lines
        orderTitle = tk.Label(self, text="Sales Lines:", font=TEXT_FONT)
        self.dynamic_buttons.append(orderTitle)
        
        orderTitle.pack()
        self.new_order.pack(fill=tk.X)

        self.spawn_orders(transfers)

        # transport lines
        transportTitle = tk.Label(self, text="Transport Lines:", font=TEXT_FONT)
        self.dynamic_buttons.append(transportTitle)

        transportTitle.pack()
        self.new_transport.pack(fill=tk.X)
        
        self.spawn_orders(transports)

        # end
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
        # I don't know why this works
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
        self.hotkeys = ["s", "p", "f", "c", "<Escape>"]
        header = tk.Label(self, text="Home", font=TITLE_FONT)
        p_profiles = tk.Button(self, text="[p] People profiles", font=BUTTON_FONT, command=lambda: controller.show_frame("people_profiles"))
        s_profiles = tk.Button(self, text="[s] Store profiles", font=BUTTON_FONT, command=lambda: controller.show_frame("store_profiles"))
        m_profiles = tk.Button(self, text="[f] Factory profiles", font=BUTTON_FONT, command=lambda: controller.show_frame("manu_profiles"))
        c_profiles = tk.Button(self, text="[c] Church profiles", font=BUTTON_FONT, command=lambda: controller.show_frame("church_profiles"))
        esc = tk.Button(self,  text="[esc] Return to Office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        p_profiles.pack(fill=tk.X)
        s_profiles.pack(fill=tk.X)
        m_profiles.pack(fill=tk.X)
        c_profiles.pack(fill=tk.X)
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
        self.root.bind("f", lambda x: self.controller.show_frame("manu_profiles"))
        self.root.bind("c", lambda x: self.controller.show_frame("church_profiles"))
        self.root.bind("<Escape>", lambda x: self.controller.show_frame("main_keyboard"))


class people_profiles(tsf.tkscrollframe):
    def __init__(self, parent, controller, root):
        tsf.tkscrollframe.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>"]
        self.dynamic_buttons  = []

        # widgets go in self.frame, not self
        header = tk.Label(self.frame, text="People Profiles", font=TITLE_FONT)
        self.esc = tk.Button(self.frame, text="[esc] Return to House", font=BUTTON_FONT, command=lambda: self.controller.show_frame("house"))
        self.esc.callback = lambda event: self.controller.show_frame("house")

        header.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.people_profiles)

    def callbackFactory(self, profile):
        def callback(event=None):
            return self.root.display_cont.display_p_profile(profile.get_values_dict())
        return callback
    
    def raise_frame(self):
        for entry in self.dynamic_buttons:
            entry.destroy()

        char = self.root.getChar()
        raw_profiles = char.getKnownPeople()
        # profiles = sorted(raw_profiles, key=attrgetter('lastname', 'firstname'))
        profiles = sorted(raw_profiles, key=attrgetter("opinion"), reverse=True)

        for profile in profiles:
            callback = self.callbackFactory(profile)
            newButton = tk.Button(self.frame, text=f"{profile.name} ({profile.opinion})", font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)

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
        self.root.bind("<Escape>", self.esc.callback)


class store_profiles(tsf.tkscrollframe):
    def __init__(self, parent, controller, root):
        tsf.tkscrollframe.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>"]
        self.dynamic_buttons = []

        #widgets go in self.frame not self
        header = tk.Label(self.frame, text="Store Profiles", font=TITLE_FONT)
        self.esc = tk.Button(self.frame, text="[esc] Return to House", font=BUTTON_FONT, command=lambda: self.controller.show_frame("house"))
        self.esc.callback = lambda event: self.controller.show_frame("house")

        header.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.store_profiles)

    def callbackFactory(self, profile):
        def callback(event=None):
            return self.root.display_cont.display_s_profile(profile.get_values_dict())
        return callback
    
    def raise_frame(self):
        for entry in self.dynamic_buttons:
            entry.destroy()

        char = self.root.getChar()
        profiles = char.getKnownStores()

        # key =1
        for profile in profiles:
            callback = self.callbackFactory(profile)
            newButton = tk.Button(self.frame, text= profile.name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)
            # key += 1

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
        self.root.bind("<Escape>", self.esc.callback)


class manu_profiles(tsf.tkscrollframe):
    def __init__(self, parent, controller, root):
        tsf.tkscrollframe.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>"]
        self.dynamic_buttons = []

        # widgets go in self.frame not self
        header = tk.Label(self.frame, text="Factory Profiles", font=TITLE_FONT)
        self.esc = tk.Button(self.frame, text="[esc] Return to House", font=BUTTON_FONT, command=lambda: self.controller.show_frame("house"))
        self.esc.callback = lambda event: self.controller.show_frame("house")

        header.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.manu_profiles)

    def callbackFactory(self, profile):
        def callback(event=None):
            return self.root.display_cont.display_m_profile(profile.get_values_dict())
        return callback
    
    def raise_frame(self):
        for entry in self.dynamic_buttons:
            entry.destroy()

        char = self.root.getChar()
        profiles = char.getKnownManus()

        for profile in profiles:
            callback = self.callbackFactory(profile)
            newButton = tk.Button(self.frame, text= profile.name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)

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
        self.root.bind("<Escape>", self.esc.callback)


class church_profiles(tsf.tkscrollframe):
    def __init__(self, parent, controller, root):
        tsf.tkscrollframe.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>"]
        self.dynamic_buttons = []

        # widgets go in self.frame not self
        header = tk.Label(self.frame, text="Church Profiles", font=TITLE_FONT)
        self.esc = tk.Button(self.frame, text="[esc] Return to House", font=BUTTON_FONT, command=lambda: self.controller.show_frame("house"))
        self.esc.callback = lambda event: self.controller.show_frame("house")

        header.pack(fill=tk.X)
        self.esc.pack(fill=tk.X)

    def show_splash(self):
        cont = self.controller.get_display_cont()
        cont.update_frame("main_display", tutorials.church_profiles)

    def callbackFactory(self, profile):
        def callback(event=None):
            return self.root.display_cont.display_c_profile(profile.get_values_dict())
        return callback
    
    def raise_frame(self):
        for entry in self.dynamic_buttons:
            entry.destroy()

        char = self.root.getChar()
        profiles = char.getKnownChurches()

        for profile in profiles:
            callback = self.callbackFactory(profile)
            newButton = tk.Button(self.frame, text= profile.name, font=BUTTON_FONT, command=callback)
            newButton.callback = callback
            newButton.pack(fill=tk.X)
            self.dynamic_buttons.append(newButton)

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
        self.root.bind("<Escape>", self.esc.callback)


class town(tk.Frame):
    def __init__(self, parent, controller, root):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.root = root
        self.hotkeys = ["<Escape>", "b", "z"]
        header = tk.Label(self, text="Town", font=TITLE_FONT)
        city_map = tk.Button(self,  text="[b] City Map", font=BUTTON_FONT, command=self.show_city_map)
        zoning_map = tk.Button(self,  text="[z] Zoning Map", font=BUTTON_FONT, command=self.show_zoning_map)
        main = tk.Button(self,  text="[esc] Return to Office", font=BUTTON_FONT, command=lambda: controller.show_frame("main_keyboard"))

        header.pack(fill=tk.X)
        city_map.pack(fill=tk.X)
        zoning_map.pack(fill=tk.X)
        main.pack(fill=tk.X)

    def show_city_map(self):
        cont = self.controller.get_display_cont()
        cont.display_map(self.get_city_map())

    def show_zoning_map(self):
        cont = self.controller.get_display_cont()
        cont.display_map(self.get_zoning_map())

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
        self.root.bind("b", lambda x: self.show_city_map())
        self.root.bind("z", lambda x: self.show_zoning_map())

    def get_city_map(self):
        char = self.root.char
        locality = char.getLocality()
        localmap = locality.get_print_map()

        return localmap

    def get_zoning_map(self):
        char = self.root.char
        locality = char.getLocality()
        localmap = locality.get_zoning_print_map()

        return localmap


class quitBar(tk.Frame):
    def __init__(self, parent, root, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = root

        aiButton = tk.Button(self,  text="Toggle AI Control", font=BUTTON_FONT, command=self.setAI)
        next_turn = tk.Button(self, text="[f1] Next Day", font=BUTTON_FONT, command=self.next_day)
        exit = tk.Button(self,      text="Quit",     font=BUTTON_FONT, command=self.quit)
        
        self.root.bind("<F1>", self.next_day)
        aiButton.pack(fill=tk.X)
        next_turn.pack(fill=tk.X)
        exit.pack(fill=tk.X)

    def next_day(self, event=None):
        char = self.root.getChar()
        self.root.text_cont.clear()
        char.run_day()
        self.root.event_generate("<<refresh>>", when="tail")

    def setAI(self, event=None):
        char = self.root.getChar()

        if char in d.bossList:
            d.removeBoss(char)
            self.root.out("\nYou have taken control of your business.\n")
        else:
            d.addBoss(char)
            self.root.out("\nYou have turned over your business to an underling.\n")

    def quit(self):
        self.root.quit()
