''' 
    This script will create and handle firing frequency gui 
    computation and aesthetic. 

    Tutorial followed from: http://zetcode.com/tkinter

    Mercedes Gonzalez. March 2020.
'''
from os import listdir
from os.path import isfile, join
from tkinter import filedialog
import tkinter as tk
import tkinter.ttk as ttk
from patchAnalysis import *


# Aesthetic params
FONTSIZE = 12

''' 
----------------------------------------------------------
LAYOUT AND DEFINITION OF ELEMENTS 
----------------------------------------------------------
'''
class myGUI(tk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main Frame Set Up
        self.master.title("Almost Real Time Patching Analysis Tool")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.pack(fill=tk.BOTH, expand=1)

        # Directory selection
        self.dir_msg = "* SELECT DIRECTORY *"
        self.dir_text = tk.StringVar()
        self.dir_text.set(self.dir_msg)

        self.dir_label = ttk.Label(self, text="Current Directory", width=16)
        self.dir_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.dir_indic = ttk.Label(self,text=self.dir_text,width=10)
        self.dir_indic.pack(fill=tk.X, padx=5, expand=True)

        # Directory mode
        self.gui_mode = 0 # 0 = auto, 1 = manual

        # Refresh Button
        refresh_btn = ttk.Button(self, text="Refresh", command=self.refreshClicked)
        refresh_btn.pack(side=tk.BOTTOM,padx=5, pady=5)
        
        # Select Button
        select_btn = ttk.Button(self, text="Select", command=self.selectDirectoryClicked)
        select_btn.pack(side=tk.BOTTOM,padx=5, pady=5)

    ''' 
    ----------------------------------------------------------
    FUNCTION DEFINITIONS
    ----------------------------------------------------------
    '''
    def refreshClicked(self):
        
        return

    def selectDirectoryClicked(self):
        current_dir = filedialog.askdirectory()
        # print(current_dir)
        self.dir_indic.set(current_dir)
        return current_dir

''' 
----------------------------------------------------------
MAIN FUNCTION
----------------------------------------------------------
'''
def main():
    root = tk.Tk()
    root.geometry("400x600+50+100") #width x height + x and y screen dims
    app = myGUI()
    root.mainloop()

if __name__ == '__main__':
    main()