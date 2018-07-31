import tkinter as tk
from tkinter import Frame, Tk, Menu, Menubutton, Label, Button, Entry, IntVar, END, W, E, filedialog
from tkinter import ttk
from tkinter import *
import os
import webbrowser

from nmapy.nmapy.nmapy_gui import texture_execution
from nmapy.nmapy.nmapy_gui import sampling_execution

class App:

    def __init__(self, master):
        self.help_url = "https://github.com/jwarndt/nmapy"

        self.master = master
        master.title("Textural Features")
        
        self.top_menu()

        # create the tabbed interface
        self.notebook = ttk.Notebook(self.master)
        self.texture_tab = ttk.Frame(self.notebook)
        self.sample_tab = ttk.Frame(self.notebook)
        self.classification_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.texture_tab, text="Textural Features")
        self.notebook.add(self.sample_tab, text="Sampling")
        self.notebook.add(self.classification_tab, text="Classification")
        self.notebook.grid(row=0, column=0,sticky='W')

        # texture parameters
        self.txt_input_entry = StringVar()
        self.txt_output_entry = StringVar()
        self.sf = StringVar()
        self.block_entry = IntVar()
        self.scale_entry = StringVar()
        self.glcm_prop = StringVar()
        self.stat = StringVar()
        self.job_num = IntVar()
        # lacunarity
        self.box_size_entry = IntVar()
        self.slide_style_entry = IntVar()
        self.lac_type = StringVar()
        # MBI
        self.postprocess = StringVar()
        # LBP
        self.radius = IntVar()
        self.n_points = IntVar()
        self.lbp_method = StringVar()
        

        # sampling parameters
        self.st = StringVar()
        self.smp_input_entry = StringVar()
        self.smp_output_entry = StringVar()
        self.input_dir_entry = StringVar()
        self.output_dir_entry = StringVar()
        self.ppc_entry = IntVar()
        self.cpf_entry = IntVar()
        self.ppf_entry = IntVar()
        self.dim_entry = IntVar()
        self.trial_entry = IntVar()

        # classification parameters

        self.build_texture_params()
        self.build_sampling_params()
        # self.build_classification_params()

    def top_menu(self):
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Close")

        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.open_help)
        helpmenu.add_command(label="About...")
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)

    def open_help(self):
        webbrowser.open_new(self.help_url)

    def build_texture_params(self):
        self.txt_input_label = Label(self.texture_tab, text="Input image")
        self.txt_output_label = Label(self.texture_tab, text="Output image")
        self.txt_input_label.grid(row=1, column=0, padx=10, sticky='W')
        self.txt_output_label.grid(row=3, column=0, padx=10, sticky='W')
        self.txt_in_file = tk.StringVar()

        self.txt_input_entry = Entry(self.texture_tab, textvariable=self.txt_in_file, width=75)
        self.txt_input_entry.grid(row=2, column=0, padx=10, sticky='W')
        # self.bbutton = Button(self.texture_tab, text="Browse", command=self.browse_for_file)
        # self.bbutton.grid(row=2, column=1, padx=10)

        self.txt_output_entry = Entry(self.texture_tab, width=75)
        self.txt_output_entry.grid(row=4, column=0, padx=10, sticky='W')

        self.sfvar = None
        spatial_feature = Label(self.texture_tab, text="Spatial/Textural feature")
        spatial_feature.grid(row=5, column=0, padx=10, sticky='W')
        options = ("HOG", "GLCM", "Pantex", "MBI", "Lacunarity", "LBP", "SIFT", "Textons", "Gabor Filters")
        self.sf = ttk.Combobox(self.texture_tab, width=75, values=options)
        self.sf.grid(row=6, column=0, columnspan=20, padx=10, sticky='W')
        self.sf.bind("<<ComboboxSelected>>", self.set_additional_texture_params)

        self.job_num.set(1)
        njob_label = Label(self.texture_tab, text="Number of jobs")
        njob_label.grid(row=50, column=0, padx=10, stick="W")
        self.njob_entry = Entry(self.texture_tab, textvariable=self.job_num, width=10)
        self.njob_entry.grid(row=51, column=0, padx=10, stick="W")

        self.txt_execute_button = Button(self.texture_tab, text="OK", command=self.run_texture_params)
        self.txt_execute_button.grid(row=51, column=0)

    def build_sampling_params(self):
        sample_type = Label(self.sample_tab, text="Training sample type")
        sample_type.grid(row=1, column=0, padx=10, sticky='W')
        options = ("Random points", "Image chips", "Square boxes")
        self.st = ttk.Combobox(self.sample_tab, width=75, values=options)
        self.st.grid(row=2, column=0, columnspan=20, padx=10, sticky='W')
        self.st.bind("<<ComboboxSelected>>", self.set_additional_sample_params)

        self.samp_execute_button = Button(self.sample_tab, text="OK", command=self.run_sample_params)
        self.samp_execute_button.grid(row=51, pady=10)

    def set_additional_texture_params(self, callback):
        self.clear_params("texture")
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

            self.stat_label = Label(self.texture_tab, text="Statistic")
            self.stat_label.grid(row=11, column=0, padx=10, sticky="W")
            stat_options = (None,"all", "min", "max", "mean", "var", "std", "sum")
            self.stat = ttk.Combobox(self.texture_tab, width=75, values=stat_options)
            self.stat.current(0)
            self.stat.grid(row=12, column=0, columnspan=20, padx=10, sticky="W")

            self.glcm_prop_label = Label(self.texture_tab, text="GLCM property")
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

            self.stat_label = Label(self.texture_tab, text="Statistic")
            self.stat_label.grid(row=11, column=0, padx=10, sticky="W")
            stat_options = (None, "all", "min", "max", "mean", "var", "std", "sum")
            self.stat = ttk.Combobox(self.texture_tab, width=75, values=stat_options)
            self.stat.current(0)
            self.stat.grid(row=12, column=0, columnspan=20, padx=10, sticky="W")

        if self.sf.get() == "MBI":
            self.postprocess_label = Label(self.texture_tab, text="Postprocess")
            self.postprocess_label.grid(row=11, column=0, padx=10, sticky="W")
            mbi_options = (True, False)
            self.postprocess = ttk.Combobox(self.texture_tab, width=75, values=mbi_options)
            self.postprocess.current(0)
            self.postprocess.grid(row=12, column=0, columnspan=20, padx=10, sticky='W')

        if self.sf.get() == "LBP":
            self.block = Label(self.texture_tab, text="Block size (pixels)")
            self.scale = Label(self.texture_tab, text='Scale size (pixels)')
            self.block.grid(row=7, column=0, ipadx=10, sticky='W')
            self.scale.grid(row=9, column=0, ipadx=10, sticky='W')
            self.block_entry = Entry(self.texture_tab, width=75)
            self.scale_entry = Entry(self.texture_tab, width=75)
            self.block_entry.grid(row=8, column=0, padx=10, sticky='W')
            self.scale_entry.grid(row=10, column=0, padx=10, sticky='W')

            self.lbp_method_label = Label(self.texture_tab, text="Method")  
            self.lbp_method_label.grid(row=11, column=0, padx=10, sticky="W")
            lbp_options = ("default", "ror", "uniform", "var")
            self.lbp_method = ttk.Combobox(self.texture_tab, width=75, values=lbp_options)
            self.lbp_method.current(0)
            self.lbp_method.grid(row=12, column=0, columnspan=20, padx=10, sticky="W")

            self.radius_label = Label(self.texture_tab, text="Radius")
            self.radius_label.grid(row=13, column=0, padx=10, sticky="W")
            self.radius = Entry(self.texture_tab, width=75)
            self.radius.grid(row=14, column=0, padx=10, sticky="W")

            self.n_points_label = Label(self.texture_tab, text="Number of points")
            self.n_points_label.grid(row=15, column=0, padx=10, sticky="W")
            self.n_points = Entry(self.texture_tab, width=75)
            self.n_points.grid(row=16, column=0, padx=10, sticky="W")

            self.stat_label = Label(self.texture_tab, text="Statistic")
            self.stat_label.grid(row=17, column=0, padx=10, sticky="W")
            stat_options = (None, "all", "min", "max", "mean", "var", "std", "sum")
            self.stat = ttk.Combobox(self.texture_tab, width=75, values=stat_options)
            self.stat.current(0)
            self.stat.grid(row=18, column=0, columnspan=20, padx=10, sticky="W")

    def set_additional_sample_params(self, callback):
        self.clear_params("sampling")
        if self.st.get() == "Random points":
            self.smp_in_file = tk.StringVar()

            self.smp_input_shapefile = Label(self.sample_tab, text="Input shapefile")
            self.smp_input_shapefile.grid(row=3, column=0, padx=10, sticky='W')
            self.smp_input_entry = Entry(self.sample_tab, textvariable=self.smp_in_file, width=75)
            self.smp_input_entry.grid(row=4, column=0, padx=10, sticky='W')

            # self.bbutton = Button(self.sample_tab, text="Browse", command=self.browse_for_file)
            # self.bbutton.grid(row=4, column=1, padx=10)

            self.smp_output_shapefile = Label(self.sample_tab, text="Output shapefile")
            self.smp_output_shapefile.grid(row=5, column=0, padx=10, sticky='W')
            self.smp_output_entry = Entry(self.sample_tab, width=75)
            self.smp_output_entry.grid(row=6, column=0, padx=10, sticky='W')

            self.ppc = Label(self.sample_tab, text="Points per class")
            self.ppc.grid(row=7, column=0, padx=10, sticky="W")
            self.ppc_entry = Entry(self.sample_tab, width=75)
            self.ppc_entry.grid(row=8, column=0, padx=10, sticky="W")

        elif self.st.get() == "Image chips":
            self.smp_in_image = tk.StringVar()
            self.smp_in_file = tk.StringVar()
            self.smp_input_dir = Label(self.sample_tab, text="Input image directory")
            self.smp_input_dir.grid(row=3, column=0, padx=10, sticky="W")
            self.smp_input_dir_entry = Entry(self.sample_tab, textvariable=self.smp_in_image, width=75)
            self.smp_input_dir_entry.grid(row=4, column=0, padx=10, sticky="W")

            # self.bbutton = Button(self.sample_tab, text="Browse", command=self.browse_for_file)
            # self.bbutton.grid(row=4, column=1, padx=10)

            self.smp_input_shapefile = Label(self.sample_tab, text="Input shapefile")
            self.smp_input_shapefile.grid(row=5, column=0, padx=10, sticky='W')
            self.smp_input_entry = Entry(self.sample_tab, textvariable=self.smp_in_file, width=75)
            self.smp_input_entry.grid(row=6, column=0, padx=10, sticky='W')

            self.smp_output_dir = Label(self.sample_tab, text="Output image directory")
            self.smp_output_dir.grid(row=7, column=0, padx=10, sticky='W')
            self.smp_output_dir_entry = Entry(self.sample_tab, width=75)
            self.smp_output_dir_entry.grid(row=8, column=0, padx=10, sticky='W')

            # chips per feature
            self.cpf = Label(self.sample_tab, text="Image chips per shapefile feature")
            self.cpf.grid(row=9, column=0, padx=10, sticky="W")
            self.cpf_entry = Entry(self.sample_tab, width=75)
            self.cpf_entry.grid(row=10, column=0, padx=10, sticky="W")

            # dimensions (pixels)
            self.dim = Label(self.sample_tab, text="Chip dimension (pixels)")
            self.dim.grid(row=11, column=0, padx=10, sticky="W")
            self.dim_entry = Entry(self.sample_tab, width=75)
            self.dim_entry.grid(row=12, column=0, padx=10, sticky="W")

            # number of trials to try and create a chip that is within a shapefile feature
            self.trials = Label(self.sample_tab, text="Number of trials")
            self.trials.grid(row=13, column=0, padx=10, sticky="W")
            self.trial_entry = Entry(self.sample_tab, width=75)
            self.trial_entry.grid(row=14, column=0, padx=10, sticky="W")

        elif self.st.get() == "Square boxes":
            self.smp_in_file = StringVar()
            self.smp_input_shapefile = Label(self.sample_tab, text="Input shapefile")
            self.smp_input_shapefile.grid(row=3, column=0, padx=10, sticky='W')
            self.smp_input_entry = Entry(self.sample_tab, textvariable=self.smp_in_file, width=75)
            self.smp_input_entry.grid(row=4, column=0, padx=10, sticky='W')

            # self.bbutton = Button(self.sample_tab, text="Browse", command=self.browse_for_file)
            # self.bbutton.grid(row=4, column=1, padx=10)
            
            self.smp_output_shapefile = Label(self.sample_tab, text="Output shapefile")
            self.smp_output_shapefile.grid(row=5, column=0, padx=10, sticky='W')
            self.smp_output_entry = Entry(self.sample_tab, width=75)
            self.smp_output_entry.grid(row=6, column=0, padx=10, sticky='W')

            self.ppf = Label(self.sample_tab, text="Plots per shapefile feature")
            self.ppf.grid(row=7, column=0, padx=10, sticky="W")
            self.ppf_entry = Entry(self.sample_tab, width=75)
            self.ppf_entry.grid(row=8, column=0, padx=10, sticky="W")

            self.dim = Label(self.sample_tab, text="Plot dimension (meters)")
            self.dim.grid(row=9, column=0, padx=10, sticky="W")
            self.dim_entry = Entry(self.sample_tab, width=75)
            self.dim_entry.grid(row=10, column=0, padx=10, sticky="W")

            # number of trials to try and create a plot that is within a shapefile feature
            self.trials = Label(self.sample_tab, text="Number of trials")
            self.trials.grid(row=11, column=0, padx=10, sticky="W")
            self.trial_entry = Entry(self.sample_tab, width=75)
            self.trial_entry.grid(row=12, column=0, padx=10, sticky="W")

    def clear_params(self, tab):
        """
        clears all parameters except input and output image
        """
        if tab == "texture":
            for label in self.texture_tab.grid_slaves():
                if int(label.grid_info()["row"]) > 6 and int(label.grid_info()["row"]) != 50 and int(label.grid_info()["row"]) != 51:
                    label.grid_forget()
        elif tab == "sampling":
            for label in self.sample_tab.grid_slaves():
                if int(label.grid_info()["row"]) > 2 and int(label.grid_info()["row"]) != 50 and int(label.grid_info()["row"]) != 51:
                    label.grid_forget()

    def run_texture_params(self):
        params = {"input": self.txt_input_entry.get(),
                  "output":self.txt_output_entry.get(),
                  "feature":self.sf.get(),
                  "block":int(self.block_entry.get()),
                  "scale":self.scale_entry.get(),
                  "prop":self.glcm_prop.get(),
                  "box_size":int(self.box_size_entry.get()),
                  "slide_style":int(self.slide_style_entry.get()),
                  "lac_type":self.lac_type.get(),
                  "stat":self.stat.get(),
                  "postprocess":self.postprocess.get(),
                  "lbp_method":self.lbp_method.get(),
                  "radius":self.radius.get(),
                  "n_points":self.n_points.get(),
                  "jobs":int(self.njob_entry.get())}
        texture_execution.execute(params)

    def run_sample_params(self):
        params = {"sample_type": self.st.get(),
                  "input_shp": self.smp_input_entry.get(),
                  "output_shp": self.smp_output_entry.get(),
                  "input_imdir": self.smp_input_dir_entry.get(),
                  "output_imdir": self.smp_output_dir_entry.get(),
                  "ppc": self.ppc_entry.get(),
                  "cpf": self.cpf_entry.get(),
                  "ppf": self.ppf_entry.get(),
                  "dim": self.dim_entry.get(),
                  "trials": self.trial_entry.get()}
        sampling_execution.execute(params)

def main():
    root = Tk()
    root.geometry('600x500')
    my_gui = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()