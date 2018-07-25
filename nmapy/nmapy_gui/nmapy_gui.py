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

        self.notebook = ttk.Notebook(self.master)
        self.texture_tab = ttk.Frame(self.notebook)
        self.sample_tab = ttk.Frame(self.notebook)
        self.classification_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.texture_tab, text="Textural Features")
        self.notebook.add(self.sample_tab, text="Sampling")
        self.notebook.add(self.classification_tab, text="Classification")
        self.notebook.grid(row=0, column=0,sticky='W')
        # self.notebook.bind("<<NotebookTabChanged>>", self.change_window)

        # related to texture parameters
        self.input_entry = StringVar()
        self.output_entry = StringVar()
        self.sf = StringVar()
        self.block_entry = IntVar()
        self.scale_entry = IntVar()
        self.glcm_prop = StringVar()
        self.box_size_entry = IntVar()
        self.slide_style_entry = IntVar()
        self.lac_type = StringVar()
        self.stat = StringVar()
        self.postprocess = BooleanVar()
        self.job_num = IntVar()

        # sampling parameters
        self.st = StringVar()
        self.in_image = StringVar()
        self.cpf_num = IntVar()
        self.dim_num = IntVar()
        self.trial_num = IntVar()

        self.build_texture_params()
        self.build_sampling_params()

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

    def build_sampling_params(self):
        sample_type = Label(self.sample_tab, text="Training sample type")
        sample_type.grid(row=1, column=0, padx=10, sticky='W')
        options = ("Random points", "Image chips", "Square boxes")
        self.st = ttk.Combobox(self.sample_tab, width=75, values=options)
        self.st.grid(row=2, column=0, columnspan=20, padx=10, sticky='W')
        self.st.bind("<<ComboboxSelected>>", self.set_additional_sample_options)

        self.execute_button = Button(self.sample_tab, text="OK", command=self.run_sample_params)
        self.execute_button.grid(row=51, pady=10)

    def set_additional_sample_options(self, callback):
        self.clear_sample_params()
        if self.st.get() == "Random points":
            self.input_shapefile = Label(self.sample_tab, text="Input shapefile")
            self.output_shapefile = Label(self.sample_tab, text="Output shapefile")
            self.input_shapefile.grid(row=3, column=0, padx=10, sticky='W')
            self.output_shapefile.grid(row=5, column=0, padx=10, sticky='W')

            self.input_entry = Entry(self.sample_tab, textvariable=self.in_file, width=75)
            self.input_entry.grid(row=4, column=0, padx=10, sticky='W')
            self.bbutton = Button(self.sample_tab, text="Browse", command=self.browse_for_file)
            self.bbutton.grid(row=4, column=1, padx=10)
            self.output_entry = Entry(self.sample_tab, width=75)
            self.output_entry.grid(row=6, column=0, padx=10, sticky='W')

            self.ppc = Label(self.sample_tab, text="Points per class")
            self.ppc.grid(row=7, column=0, padx=10, sticky="W")
            self.ppc_entry = Entry(self.sample_tab, width=75)
            self.ppc_entry.grid(row=8, column=0, padx=10, sticky="W")

        elif self.st.get() == "Image chips":
            self.input_image = Label(self.sample_tab, text="Input image directory")
            self.input_image.grid(row=3, column=0, padx=10, sticky="W")
            self.input_image_entry = Entry(self.sample_tab, textvariable=self.in_image, width=75)
            self.input_image_entry.grid(row=4, column=0, padx=10, sticky="W")

            self.bbutton = Button(self.sample_tab, text="Browse", command=self.browse_for_file)
            self.bbutton.grid(row=4, column=1, padx=10)

            self.input_shapefile = Label(self.sample_tab, text="Input shapefile")
            self.input_shapefile.grid(row=5, column=0, padx=10, sticky='W')
            self.input_entry = Entry(self.sample_tab, textvariable=self.in_file, width=75)
            self.input_entry.grid(row=6, column=0, padx=10, sticky='W')

            self.output_dir = Label(self.sample_tab, text="Output image directory")
            self.output_dir.grid(row=7, column=0, padx=10, sticky='W')
            self.output_entry = Entry(self.sample_tab, width=75)
            self.output_entry.grid(row=8, column=0, padx=10, sticky='W')
           

            # chips per feature
            self.cpf = Label(self.sample_tab, text="Image chips per shapefile feature")
            self.cpf.grid(row=9, column=0, padx=10, sticky="W")
            self.cpf_entry = Entry(self.sample_tab, textvariable=self.cpf_num, width=75)
            self.cpf_entry.grid(row=10, column=0, padx=10, sticky="W")

            # dimensions (pixels)
            self.dim = Label(self.sample_tab, text="Chip dimension (pixels)")
            self.dim.grid(row=11, column=0, padx=10, sticky="W")
            self.dim_entry = Entry(self.sample_tab, textvariable=self.dim_num, width=75)
            self.dim_entry.grid(row=12, column=0, padx=10, sticky="W")

            # number of trials to try and create a chip that is within a shapefile feature
            self.trials = Label(self.sample_tab, text="Number of trials")
            self.trials.grid(row=13, column=0, padx=10, sticky="W")
            self.trial_entry = Entry(self.sample_tab, textvariable=self.trial_num, width=75)
            self.trial_entry.grid(row=14, column=0, padx=10, sticky="W")

        elif self.st.get() == "Square boxes":
            self.input_shapefile = Label(self.sample_tab, text="Input shapefile")
            self.output_shapefile = Label(self.sample_tab, text="Output shapefile")
            self.input_shapefile.grid(row=3, column=0, padx=10, sticky='W')
            self.output_shapefile.grid(row=5, column=0, padx=10, sticky='W')

            self.input_entry = Entry(self.sample_tab, textvariable=self.in_file, width=75)
            self.input_entry.grid(row=4, column=0, padx=10, sticky='W')
            self.bbutton = Button(self.sample_tab, text="Browse", command=self.browse_for_file)
            self.bbutton.grid(row=4, column=1, padx=10)
            self.output_entry = Entry(self.sample_tab, width=75)
            self.output_entry.grid(row=6, column=0, padx=10, sticky='W')
        
    def build_texture_params(self):
        self.input_label = Label(self.texture_tab, text="Input image")
        self.output_label = Label(self.texture_tab, text="Output image")
        self.input_label.grid(row=1, column=0, padx=10, sticky='W')
        self.output_label.grid(row=3, column=0, padx=10, sticky='W')
        self.in_file = tk.StringVar()

        self.input_entry = Entry(self.texture_tab, textvariable=self.in_file, width=75)
        self.input_entry.grid(row=2, column=0, padx=10, sticky='W')
        self.bbutton = Button(self.texture_tab, text="Browse", command=self.browse_for_file)
        self.bbutton.grid(row=2, column=1, padx=10)

        self.output_entry = Entry(self.texture_tab, width=75)
        self.output_entry.grid(row=4, column=0, padx=10, sticky='W')

        self.sfvar = None
        spatial_feature = Label(self.texture_tab, text="Spatial/Textural feature")
        spatial_feature.grid(row=5, column=0, padx=10, sticky='W')
        options = ("HOG", "GLCM", "Pantex", "MBI", "Lacunarity", "SIFT", "DSIFT", "Textons")
        self.sf = ttk.Combobox(self.texture_tab, width=75, values=options)
        self.sf.grid(row=6, column=0, columnspan=20, padx=10, sticky='W')
        self.sf.bind("<<ComboboxSelected>>", self.set_additional_texture_options)

        self.job_num.set(1)
        njob_label = Label(self.texture_tab, text="Number of jobs")
        njob_label.grid(row=50, column=0, padx=10, stick="W")
        self.njob_entry = Entry(self.texture_tab, textvariable=self.job_num, width=10)
        self.njob_entry.grid(row=51, column=0, padx=10, stick="W")

        self.execute_button = Button(self.texture_tab, text="OK", command=self.run_texture_params)
        self.execute_button.grid(row=51, column=0)


    def browse_for_file(self):
        Tk().withdraw()
        filename = filedialog.askopenfilename()
        self.in_file.set(filename)

    def clear_texture_params(self):
        """
        clears all parameters except input and output image
        """
        for label in self.texture_tab.grid_slaves():
            if int(label.grid_info()["row"]) > 6 and int(label.grid_info()["row"]) != 50 and int(label.grid_info()["row"]) != 51:
                label.grid_forget()

    def clear_sample_params(self):
        """
        clears all parameters except input and output image
        """
        for label in self.sample_tab.grid_slaves():
            if int(label.grid_info()["row"]) > 2 and int(label.grid_info()["row"]) != 50 and int(label.grid_info()["row"]) != 51:
                label.grid_forget()

    def set_additional_texture_options(self, callback):
        self.clear_texture_params()
        if self.sf.get() == "Pantex":
            self.block = Label(self.texture_tab, text="Block size (pixels)")
            self.scale = Label(self.texture_tab, text='Scale size (pixels)')
            self.block.grid(row=7, column=0, ipadx=10, sticky='W')
            self.scale.grid(row=9, column=0, ipadx=10, sticky='W')
            self.block_entry = Entry(self.texture_tab, width=75)
            self.scale_entry = Entry(self.texture_tab,  width=75)
            self.block_entry.grid(row=8, column=0, padx=10, sticky='W')
            self.scale_entry.grid(row=10, column=0, padx=10, sticky='W')

        if self.sf.get() == "Lacunarity":
            self.block = Label(self.texture_tab, text="Block size (pixels)")
            self.scale = Label(self.texture_tab, text='Scale size (pixels)')
            self.block.grid(row=7, column=0, ipadx=10, sticky='W')
            self.scale.grid(row=9, column=0, ipadx=10, sticky='W')
            self.block_entry = Entry(self.texture_tab, width=75)
            self.scale_entry = Entry(self.texture_tab, width=75)
            self.block_entry.grid(row=8, column=0, padx=10, sticky='W')
            self.scale_entry.grid(row=10, column=0, padx=10, sticky='W')

            self.box_size_label= Label(self.texture_tab, text="Box size")
            self.box_size_label.grid(row=11, column=0, padx=10, sticky='W')
            self.box_size_entry = Entry(self.texture_tab, width=75)
            self.box_size_entry.grid(row=12, column=0, columnspan=20, padx=10, sticky='W')
            
            self.slide_style_label= Label(self.texture_tab, text="Slide style")
            self.slide_style_label.grid(row=13, column=0, padx=10, sticky='W')
            self.slide_style_entry = Entry(self.texture_tab, width=75)
            self.slide_style_entry.grid(row=14, column=0, columnspan=20, padx=10, sticky='W')

            self.lac_type_label= Label(self.texture_tab, text="Lacunarity type")
            self.lac_type_label.grid(row=15, column=0, padx=10, sticky='W')
            options = ("grayscale", "binary")
            self.lac_type = ttk.Combobox(self.texture_tab, width=75, values=options)
            self.lac_type.current(0)
            self.lac_type.grid(row=16, column=0, columnspan=20, padx=10, sticky='W')            

        if self.sf.get() == "GLCM":
            self.block = Label(self.texture_tab, text="Block size (pixels)")
            self.scale = Label(self.texture_tab, text='Scale size (pixels)')
            self.block.grid(row=7, column=0, ipadx=10, sticky='W')
            self.scale.grid(row=9, column=0, ipadx=10, sticky='W')
            self.block_entry = Entry(self.texture_tab, width=75)
            self.scale_entry = Entry(self.texture_tab, width=75)
            self.block_entry.grid(row=8, column=0, padx=10, sticky='W')
            self.scale_entry.grid(row=10, column=0, padx=10, sticky='W')

            self.stat_label = Label(self.texture_tab, text="Statistic (optional)")
            self.stat_label.grid(row=11, column=0, padx=10, sticky="W")
            stat_options = (None,"all", "min", "max", "mean", "var", "std", "sum")
            self.stat = ttk.Combobox(self.texture_tab, width=75, values=stat_options)
            self.stat.current(0)
            self.stat.grid(row=12, column=0, columnspan=20, padx=10, sticky="W")

            self.glcm_prop_label = Label(self.texture_tab, text="GLCM property (optional)")
            self.glcm_prop_label.grid(row=13, column=0, padx=10, sticky='W')
            prop_options = (None,"contrast", "dissimilarity", "homogeneity", "ASM", "energy", "correlation")
            self.glcm_prop = ttk.Combobox(self.texture_tab, width=75, values=prop_options)
            self.glcm_prop.current(0)
            self.glcm_prop.grid(row=14, column=0, columnspan=20, padx=10, sticky="W")

        if self.sf.get() == "HOG":
            self.block = Label(self.texture_tab, text="Block size (pixels)")
            self.scale = Label(self.texture_tab, text='Scale size (pixels)')
            self.block.grid(row=7, column=0, ipadx=10, sticky='W')
            self.scale.grid(row=9, column=0, ipadx=10, sticky='W')
            self.block_entry = Entry(self.texture_tab, width=75)
            self.scale_entry = Entry(self.texture_tab, width=75)
            self.block_entry.grid(row=8, column=0, padx=10, sticky='W')
            self.scale_entry.grid(row=10, column=0, padx=10, sticky='W')

            self.stat_label = Label(self.texture_tab, text="Statistic (optional)")
            self.stat_label.grid(row=11, column=0, padx=10, sticky="W")
            stat_options = (None, "all", "min", "max", "mean", "var", "std", "sum")
            self.stat = ttk.Combobox(self.texture_tab, width=75, values=stat_options)
            self.stat.current(0)
            self.stat.grid(row=12, column=0, columnspan=20, padx=10, sticky="W")

        if self.sf.get() == "MBI":
            self.postprocess_label = Label(self.texture_tab, text="Postprocess")
            self.postprocess_label.grid(row=11, column=0, padx=10, sticky="W")
            options = (True, False)
            self.postprocess = ttk.Combobox(self.texture_tab, width=75, values=options)
            self.postprocess.current(0)
            self.postprocess.grid(row=12, column=0, columnspan=20, padx=10, sticky='W')  

    def run_texture_params(self):
        params = {"input": self.input_entry.get(),
                  "output":self.output_entry.get(),
                  "feature":self.sf.get(),
                  "block":int(self.block_entry.get()),
                  "scale":int(self.scale_entry.get()),
                  "prop":self.glcm_prop.get(),
                  "box_size":int(self.box_size_entry.get()),
                  "slide_style":int(self.slide_style_entry.get()),
                  "lac_type":self.lac_type.get(),
                  "stat":self.stat.get(),
                  "postprocess":self.postprocess.get(),
                  "jobs":int(self.njob_entry.get())}
        execute(params)

    def run_sample_params(self):
        params = {}

def main():
    root = Tk()
    root.geometry('600x300')
    my_gui = TexturalFeatures(root)
    root.mainloop()

if __name__ == "__main__":
    main()