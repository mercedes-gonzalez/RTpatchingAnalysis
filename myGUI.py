import tkinter as tk 
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
import csv
import numpy as np
import scipy as sp
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
        # DEFINE: CONTAINERS

        # File list
        # self.abffiles = [None]
        # scrollbar = tk.Scrollbar(master,orient=tk.VERTICAL)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.abffile_box = tk.Listbox(master) #yscrollcommand=scrollbar.set)
        # scrollbar.config(command=self.abffile_box.yview)
        

        # Directory handling
        self.directory = "* SET DIRECTORY *"
        self.directory_label_text = tk.StringVar()
        self.directory_label_text.set(self.directory)
        self.directory_display = tk.Label(master, textvariable=self.directory_label_text)
        self.directory_label = tk.Label(master, text="Directory:")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = tk.Entry(master, validate="key", validatecommand=(vcmd, '%P'))


        # DEFINE: BUTTONS
        self.select_button = tk.Button(master, text="Select", command=lambda: self.update("select"))
        self.reset_button = tk.Button(master, text="Reset", command=lambda: self.update("reset"))
        
        # LAYOUT: CONTAINERS
        self.directory_label.grid(sticky=tk.NW)
        self.directory_display.grid(sticky=tk.NE)
        self.abffile_box.grid(sticky=tk.W)
        self.entry.grid(sticky=tk.S)

        # LAYOUT: BUTTONS
        self.reset_button.grid(sticky=tk.SE)
        self.select_button.grid(sticky=tk.SE)

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
            for item in self.abf_files:
                self.abffile_box.insert(tk.END,item)

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
    - plot box
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
    -proper container placement

    DONE
    - select button to select directory
    - display current directory
    - reset button    
    - read all files from the selected directory
    - display file names in listbox 

'''