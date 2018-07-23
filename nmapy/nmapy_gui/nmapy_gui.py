import tkinter as tk
from tkinter import Frame, Tk, Menu, Menubutton, Label, Button, Entry, IntVar, END, W, E, filedialog
from tkinter import ttk
from tkinter import *
import os

from nmapy.nmapy.nmapy_gui.execution import *

class TexturalFeatures:

    def __init__(self, master):
        self.master = master
        master.title("Textural Features")
        
        self.top_menu()

        self.input_entry = StringVar()
        self.output_entry = StringVar()
        self.sf = StringVar()
        self.block_entry = IntVar()
        self.scale_entry = IntVar()
        self.glcm_prop = StringVar()
        self.box_size_entry = IntVar()
        self.slide_style_entry = IntVar()
        self.stat = StringVar()
        self.postprocess = BooleanVar()
        
        self.input_label = Label(master, text="Input image")
        self.output_label = Label(master, text="Output image")
        self.input_label.grid(row=0, column=0, padx=10, sticky='W')
        self.output_label.grid(row=2, column=0, padx=10, sticky='W')
        self.block = Label(master, text="Block size (pixels)")
        self.scale = Label(master, text='Scale size (pixels)')
        self.block.grid(row=6, column=0, ipadx=10, sticky='W')
        self.scale.grid(row=8, column=0, ipadx=10, sticky='W')

        self.in_file = tk.StringVar()

        vcmd = master.register(self.validate) # we have to wrap the command
        self.input_entry = Entry(master, textvariable=self.in_file, width=75, validate="key", validatecommand=(vcmd, '%P'))
        self.input_entry.grid(row=1, column=0, padx=10, sticky='W')
        photo=PhotoImage(file="C:/Users/Jacob/Projects/open-file.png")
        self.bbutton = Button(master, image=photo, command=self.browse_for_file)
        self.bbutton.image = photo
        self.bbutton.grid(row=1, column=1)

        self.output_entry = Entry(master, validate="key", width=75, validatecommand=(vcmd, '%P'))
        self.output_entry.grid(row=3, column=0, padx=10, sticky='W')
        self.block_entry = Entry(master, validate="key", width=75, validatecommand=(vcmd, '%P'))
        self.scale_entry = Entry(master, validate="key", width=75, validatecommand=(vcmd, '%P'))
        self.block_entry.grid(row=7, column=0, padx=10, sticky='W')
        self.scale_entry.grid(row=9, column=0, padx=10, sticky='W')

        self.sfvar = None
        self.spatial_feature_menu()

        self.execute_button = Button(master, text="OK", command=lambda: self.run_params())
        self.execute_button.grid(row=50, column=0, pady=10)

    def browse_for_file(self):
        Tk().withdraw()
        filename = filedialog.askopenfilename()
        self.in_file.set(filename)

    def top_menu(self):
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...")
        filemenu.add_command(label="Close")

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo")

        editmenu.add_separator()

        editmenu.add_command(label="Cut")
        editmenu.add_command(label="Copy")
        editmenu.add_command(label="Paste")
        editmenu.add_command(label="Delete")
        editmenu.add_command(label="Select All")

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index")
        helpmenu.add_command(label="About...")
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)


    def set_additional_options(self, callback):
        if self.sf.get() == "Lacunarity":
            self.box_size_label= Label(self.master, text="Box size")
            self.box_size_label.grid(row=10, column=0, padx=10, sticky='W')
            self.box_size_entry = Entry(self.master, width=75, validate="key")
            self.box_size_entry.grid(row=11, column=0, columnspan=20, padx=10, sticky='W')
            
            self.slide_style_label= Label(self.master, text="Slide style")
            self.slide_style_label.grid(row=12, column=0, padx=10, sticky='W')
            self.slide_style_entry = Entry(self.master, width=75, validate="key")
            self.slide_style_entry.grid(row=13, column=0, columnspan=20, padx=10, sticky='W')

            self.lac_type_label= Label(self.master, text="Lacunarity type")
            self.lac_type_label.grid(row=14, column=0, padx=10, sticky='W')
            options = ("grayscale", "binary")
            self.lac_type = ttk.Combobox(self.master, width=75, values=options)
            self.lac_type.current(0)
            self.lac_type.grid(row=15, column=0, columnspan=20, padx=10, sticky='W')            

        if self.sf.get() == "GLCM":
            self.stat_label = Label(self.master, text="Statistic (optional)")
            self.stat_label.grid(row=10, column=0, padx=10, sticky="W")
            stat_options = (None,"all", "min", "max", "mean", "var", "std", "sum")
            self.stat = ttk.Combobox(self.master, width=75, values=stat_options)
            self.stat.current(0)
            self.stat.grid(row=11, column=0, columnspan=20, padx=10, sticky="W")

            self.glcm_prop_label = Label(self.master, text="GLCM property (optional)")
            self.glcm_prop_label.grid(row=12, column=0, padx=10, sticky='W')
            prop_options = (None,"contrast", "dissimilarity", "homogeneity", "ASM", "energy", "correlation")
            self.glcm_prop = ttk.Combobox(self.master, width=75, values=prop_options)
            self.glcm_prop.current(0)
            self.glcm_prop.grid(row=13, column=0, columnspan=20, padx=10, sticky="W")

        if self.sf.get() == "HOG":
            self.stat_label = Label(self.master, text="Statistic (optional)")
            self.stat_label.grid(row=10, column=0, padx=10, sticky="W")
            stat_options = (None, "all", "min", "max", "mean", "var", "std", "sum")
            self.stat = ttk.Combobox(self.master, width=75, values=stat_options)
            self.stat.current(0)
            self.stat.grid(row=11, column=0, columnspan=20, padx=10, sticky="W")

        if self.sf.get() == "MBI":
            self.postprocess_label = Label(self.master, text="Postprocess")
            self.postprocess_label.grid(row=10, column=0, padx=10, sticky="W")
            options = (True, False)
            self.postprocess = ttk.Combobox(self.master, width=75, values=options)
            self.postprocess.current(0)
            self.postprocess.grid(row=11, column=0, columnspan=20, padx=10, sticky='W')

    def spatial_feature_menu(self):
        spatial_feature = Label(self.master, text="Spatial/Textural feature")
        spatial_feature.grid(row=4, column=0, padx=10, sticky='W')

        options = ("HOG", "GLCM", "Pantex", "MBI", "Lacunarity", "SIFT", "DSIFT", "Textons")
        self.sf = ttk.Combobox(self.master, width=75, values=options)
        self.sf.grid(row=5, column=0, columnspan=20, padx=10, sticky='W')
        self.sf.bind("<<ComboboxSelected>>", self.set_additional_options)

    def run_params(self):
        params = {"input": self.input_entry.get(),
                  "output":self.output_entry.get(),
                  "feature":self.sf.get(),
                  "block":self.block_entry.get(),
                  "scale":self.scale_entry.get(),
                  "prop":self.glcm_prop.get(),
                  "box_size":self.box_size_entry.get(),
                  "slide_style":self.slide_style_entry.get(),
                  "stat":self.stat.get(),
                  "postprocess":self.postprocess.get()}
        execute(params)

    def validate(self, new_text):
        """try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False"""

def main():
    root = Tk()
    root.geometry('600x300')
    my_gui = TexturalFeatures(root)
    root.mainloop()

if __name__ == "__main__":
    main()