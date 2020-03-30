import tkinter as tk 
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
import csv
import numpy as np
import scipy as sp
import scipy.signal as sig
import pyabf
import matplotlib as plt
import axographio as axo
from patchAnalysis import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler

class patchAnalysisTool:
    def __init__(self, master):
        self.master = master
        master.title("Patching Analysis Tool")
        # DEFINE: VARIABLES
        self.input_cmd = np.empty((1,1))
        self.AP_count = np.empty((1,1))
        self.input_dur = np.empty((1,1))
        # DEFINE: CONTAINERS

        # File list
        # self.abffiles = [None]
        # scrollbar = tk.Scrollbar(master,orient=tk.VERTICAL)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.abffile_box = tk.Listbox(master) #yscrollcommand=scrollbar.set)
        # scrollbar.config(command=self.abffile_box.yview)
        
        # Plotting
        self.fig = Figure(figsize=(5, 4), dpi=100)
                
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)  # A tk.DrawingArea.
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        # Directory handling
        self.directory = "* SET DIRECTORY *"
        self.directory_label_text = tk.StringVar()
        self.directory_label_text.set(self.directory)
        self.directory_display = tk.Label(master, textvariable=self.directory_label_text)
        self.directory_label = tk.Label(master, text="Directory:")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.cap = tk.Entry(master, validate="key", validatecommand=(vcmd, '%P'))


        # DEFINE: BUTTONS
        self.select_button = tk.Button(master, text="Select", command=lambda: self.update("select"))
        self.reset_button = tk.Button(master, text="Reset", command=lambda: self.update("reset"))
        
        # LAYOUT
        self.directory_label.pack(side=tk.TOP,expand=0)
        self.directory_display.pack(side=tk.TOP,fill=tk.X,expand=0)
        self.abffile_box.pack(side=tk.LEFT,fill=tk.Y)
        self.cap.pack(side=tk.TOP)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT)
        self.reset_button.pack(side=tk.RIGHT,expand=0)
        self.select_button.pack(side=tk.RIGHT,expand=0)

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == "select":
            self.directory = filedialog.askdirectory()
            self.directory_label_text.set(self.directory)
            self.abf_files = [f for f in listdir(self.directory) if isfile(join(self.directory, f)) & f.endswith(".abf")]
            abf = pyabf.ABF(join(self.directory,self.abf_files[0]))

            for item in self.abf_files:
                self.abffile_box.insert(tk.END,item)
                self.input_cmd, self.AP_count, self.input_dur = analyzeFile(item,self)
                self.step_time = self.input_dur[0]/abf.dataRate*1000
                self.fig.add_subplot(111).plot(self.input_cmd/22,self.AP_count/self.step_time,"o")

        elif method == "reset":
            self.directory = "* SELECT DIRECTORY *"
            self.directory_label_text.set(self.directory)
            self.abf_files=[None]
            self.abffile_box.delete(0,tk.END)

root = tk.Tk()
root.geometry("600x600+50+100") #width x height + x and y screen dims
my_gui = patchAnalysisTool(root)
root.mainloop()

'''
    TODO 
    - read data from only selected files
    - plot data from selected files
        - prettify the plot
    - enable auto-updating every 5 seconds
    - interactive plot??? 
    - manual vs auto mode 
        - manual means user chooses files 
        - auto means grab all files from directory
    - save data in csv
    - save figure
    - proper container placement
        - put everything in frames
    - membtest plot and analysis

    DONE
    - select button to select directory
    - display current directory
    - reset button    
    - read all files from the selected directory
    - display file names in listbox 
    - add plot box

'''