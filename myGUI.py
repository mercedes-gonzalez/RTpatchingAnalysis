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
        DIR_FRAME = tk.Frame(self, height=50,width=600,bg='indigo').pack(side=tk.TOP,fill=tk.X)
        LIST_FRAME = tk.Frame(self, height=300,width=200,bg='violet').pack(side=tk.LEFT,fill=tk.Y)
        MODE_FRAME = tk.Frame(self, height=100,width=200,bg='orange').pack(side=tk.RIGHT,fill=tk.Y)
        CONTROLS_FRAME = tk.Frame(self, height=100,width=100,bg='yellow').pack(side=tk.RIGHT,fill=tk.Y)
        
        # DEFINE: VARIABLES
        self.input_cmd = np.empty((1,1))
        self.AP_count = np.empty((1,1))
        self.input_dur = np.empty((1,1))
        # DEFINE: CONTAINERS
        self.abffile_box = tk.Listbox(LIST_FRAME) #yscrollcommand=scrollbar.set)


        # Directory handling
        self.directory = "* SET DIRECTORY *"
        self.directory_label_text = tk.StringVar()
        self.directory_label_text.set(self.directory)
        self.directory_display = tk.Label(DIR_FRAME, textvariable=self.directory_label_text)
        self.directory_label = tk.Label(DIR_FRAME, text="Directory:")

        # Capacitance
        self.cap = 1
        self.cap_label_text = tk.IntVar()
        self.cap_label_text.set(self.cap)
        self.cap_label = tk.Label(DIR_FRAME, text="Capacitance [pF]:")

        vcmd = self.master.register(self.validate) # we have to wrap the command
        self.cap = tk.Entry(CONTROLS_FRAME, validate="key", validatecommand=(vcmd, '%P'))


        # DEFINE: BUTTONS
        self.select_button = tk.Button(CONTROLS_FRAME, text="Select", command=lambda: self.update("select"))
        self.reset_button = tk.Button(CONTROLS_FRAME, text="Reset", command=lambda: self.update("reset"))
        
        # LAYOUT
        self.directory_label.pack(side=tk.TOP,fill=tk.X,expand=0)
        self.directory_display.pack(side=tk.TOP,fill=tk.X,expand=0)
        self.abffile_box.pack(side=tk.LEFT,fill=tk.Y)
        self.cap_label.pack(side=tk.TOP,expand=0)
        self.cap.pack(side=tk.TOP,fill=tk.X,expand=0)

        self.reset_button.pack(side=tk.RIGHT,fill=tk.Y,expand=0)
        self.select_button.pack(side=tk.RIGHT,fill=tk.Y,expand=0)

    def refreshFigure(self,x,y):
        self.line1.set_data(x,y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())
        self.canvas.draw()

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
                ax = self.fig.add_subplot(111)
                ax.plot(self.input_cmd/22,self.AP_count/self.step_time,"o")
                ax.set_ylabel('Firing Frequency [Hz]')
                ax.set_xlabel('Current Density [pA/pF]')
                # self.set_ylabel('Current Density (pA/pF)')
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