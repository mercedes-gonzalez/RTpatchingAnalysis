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

class patchAnalysisTool(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        master.title("Patching Analysis Tool")
        self.master = master
        # Plotting
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)  # A tk.DrawingArea.
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()

        # Pack plot because it's not in a frame
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # DEFINE FRAMES
        self.DIR_FRAME = tk.Frame(root, height=50,width=600,bg='indigo')
        self.LIST_FRAME = tk.Frame(self.master, height=300,width=200,bg='violet')
        self.MODE_FRAME = tk.Frame(self.master, height=100,width=200,bg='orange')
        self.CONTROLS_FRAME = tk.Frame(self.master, height=100,width=100,bg='yellow')
        
        # wrapped commands
        vcmd = self.master.register(self.validate) # we have to wrap the command
        # mccmd = self.master.register(self.modeChange) # we have to wrap the modeChange command
        
        # DEFINE: VARIABLES
        self.directory = "* SET DIRECTORY *"
        self.input_cmd = np.empty((1,1))
        self.AP_count = np.empty((1,1))
        self.input_dur = np.empty((1,1))
        self.mode = tk.IntVar() # 0 is auto, 1 is manual
        self.mode.set(0)
        self.cap = 1
        self.modes = {"Auto" : "0", "Manual" : "1"}
        self.mode.trace('w', self.modeChange)

        # DEFINE: CONTAINERS
        self.abffile_box = tk.Listbox(self.LIST_FRAME,selectmode=tk.EXTENDED) #yscrollcommand=scrollbar.set)
        self.scrollbar = tk.Scrollbar(self.LIST_FRAME)
        self.scrollbar['command'] = self.abffile_box.yview
        self.abffile_box['yscrollcommand'] = self.scrollbar.set
        self.file_selection = [self.abffile_box.get(i) for i in self.abffile_box.curselection()]
        
        # Directory handling
        self.directory_label_text = tk.StringVar()
        self.directory_label_text.set(self.directory)
        self.directory_display = tk.Label(self.DIR_FRAME, textvariable=self.directory_label_text)
        self.directory_label = tk.Label(self.DIR_FRAME, text="Directory:")

        # Capacitance
        self.cap_label_text = tk.IntVar()
        self.cap_label_text.set(self.cap)
        self.cap_label = tk.Label(self.CONTROLS_FRAME, text="Capacitance [pF]:")

        self.cap = tk.Entry(self.CONTROLS_FRAME, validate="key", validatecommand=(vcmd, '%P'))

        # DEFINE: BUTTONS
        self.select_button = tk.Button(self.CONTROLS_FRAME, text="Select", command=lambda: self.update("select"))
        self.reset_button = tk.Button(self.CONTROLS_FRAME, text="Reset", command=lambda: self.update("reset"))
        for (text,value) in self.modes.items():
            tk.Radiobutton(self.MODE_FRAME,text=text,variable=self.mode,value=value).pack(anchor=tk.CENTER,ipady=5)
        
        # LAYOUT PACKING
        self.DIR_FRAME.pack(side=tk.TOP,fill=tk.X)
        self.LIST_FRAME.pack(side=tk.LEFT,fill=tk.Y)
        self.CONTROLS_FRAME.pack(side=tk.RIGHT,fill=tk.Y)
        self.MODE_FRAME.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.directory_label.pack(side=tk.TOP,expand=0)
        self.directory_display.pack(side=tk.TOP,expand=0)
        self.abffile_box.pack(side=tk.LEFT,fill=tk.Y)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.cap_label.pack(side=tk.TOP,expand=0)
        self.cap.pack(side=tk.TOP,fill=tk.X,expand=0)

        self.reset_button.pack(side=tk.RIGHT,fill=tk.Y,expand=0)
        self.select_button.pack(side=tk.RIGHT,fill=tk.Y,expand=0)

    def modeChange(self):
        self.ax = self.fig.add_subplot(111)
        self.ax.cla()
        self.ax.set_ylabel('Firing Frequency [Hz]')
        self.ax.set_xlabel('Current Density [pA/pF]')
        if self.directory != "* SET DIRECTORY *":
            if self.mode.get() == 0:
                self.ax.plot(self.input_cmd/22,self.AP_count/self.step_time,"o")
            elif self.mode.get() == 1:
                for sel in self.file_selection:
                    print(sel)
                    self.ax.plot(self.input_cmd/22,self.AP_count/self.step_time,"o")
        return

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
            self.ax = self.fig.add_subplot(111)
            self.ax.cla()
            self.ax.set_ylabel('Firing Frequency [Hz]')
            self.ax.set_xlabel('Current Density [pA/pF]')

            for item in self.abf_files:
                self.abffile_box.insert(tk.END,item)
                self.input_cmd, self.AP_count, self.input_dur = analyzeFile(item,self)
                self.step_time = self.input_dur[0]/abf.dataRate*1000
                if self.mode.get() == 0:
                    self.ax.plot(self.input_cmd/22,self.AP_count/self.step_time,"o")
            if self.mode.get() == 1:
                for sel in self.file_selection:
                    self.input_cmd, self.AP_count, self.input_dur = analyzeFile(item,self)
                    self.step_time = self.input_dur[0]/abf.dataRate*1000
                    self.ax.plot(self.input_cmd/22,self.AP_count/self.step_time,"o")
        # elif method == "auto-refresh":
        #     # do nothing
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
    - manual vs auto mode 
        - manual means user chooses files 
        - auto means grab all files from directory
    - save data in csv
    - save figure
    - membtest plot and analysis

    DONE
    - select button to select directory
    - display current directory
    - reset button    
    - read all files from the selected directory
    - display file names in listbox 
    - add plot box
    - interactive plot??? 
    - proper container placement
        - put everything in frames

'''