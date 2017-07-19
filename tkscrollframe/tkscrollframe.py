import tkinter as tk

class tkscrollframe(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        #scrollbar
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.frameConfigure()

    def onFrameConfigure(self, event=None):
        # reset scroll region to encompass inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def frameConfigure(self, event=None):
        height = self.winfo_height()
        width = self.winfo_width()
        self.canvas.configure(height=height, width=width)

if __name__ == "__main__":
	root = tk.Tk()
	frame = tkscrollframe(root, width=500, height=500)
	frame.pack(fill="both",expand=True)

	root.mainloop()